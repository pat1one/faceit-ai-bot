import logging
import os
from datetime import datetime
from io import BytesIO
from typing import Optional

import discord
from discord import app_commands
from fastapi import UploadFile
try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None  # type: ignore[assignment]

from src.server.database.connection import SessionLocal
from src.server.database.models import User
from src.server.exceptions import DemoAnalysisException
from src.server.features.player_analysis.service import PlayerAnalysisService
from src.server.features.demo_analyzer.service import DemoAnalyzer
from src.server.features.teammates.models import TeammatePreferences
from src.server.features.teammates.service import TeammateService


logger = logging.getLogger("discord_bot")
logging.basicConfig(level=logging.INFO)


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# Discord guild (server) ID – можно переопределить через переменную окружения
GUILD_ID: Optional[int] = None
_guild_env = os.getenv("DISCORD_GUILD_ID")
if _guild_env:
    try:
        GUILD_ID = int(_guild_env)
    except ValueError:
        logger.warning("Invalid DISCORD_GUILD_ID env value: %s", _guild_env)


player_service = PlayerAnalysisService()
demo_analyzer = DemoAnalyzer()
teammate_service = TeammateService()

MAX_DEMO_SIZE_MB = 200
MAX_DEMO_SIZE_BYTES = MAX_DEMO_SIZE_MB * 1024 * 1024
_SNIFF_BYTES = 4096

if REDIS_AVAILABLE:
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    try:
        redis_client = redis.from_url(
            REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
        logger.info("Discord bot rate limiting enabled via Redis")
    except Exception:
        logger.exception("Failed to connect to Redis for Discord bot rate limiting")
        redis_client = None
else:
    redis_client = None


async def check_bot_rate_limit(
    user_key: str,
    operation: str,
    limit_per_minute: int,
    limit_per_day: Optional[int] = None,
) -> bool:
    """Rate limit Discord bot commands per user.

    Returns True if allowed, False if limit exceeded.
    """
    if redis_client is None:
        return True

    try:
        key = f"rl:bot:discord:{operation}:{user_key}:minute"
        count = await redis_client.incr(key)
        if count == 1:
            await redis_client.expire(key, 60)
        if count > limit_per_minute:
            return False

        if limit_per_day is not None and limit_per_day > 0:
            day_suffix = datetime.utcnow().strftime("%Y%m%d")
            day_key = f"rl:bot:discord:{operation}:{user_key}:day:{day_suffix}"
            day_count = await redis_client.incr(day_key)
            if day_count == 1:
                await redis_client.expire(day_key, 86400)
            if day_count > limit_per_day:
                return False

        return True
    except Exception as e:
        logger.error("Discord bot rate limit error: %s", e)
        return True


@tree.command(name="hello", description="Тестовая команда")
async def hello(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("Работает!", ephemeral=True)


@tree.command(name="website", description="Ссылка на основной сайт")
async def website(interaction: discord.Interaction) -> None:
    embed = discord.Embed(
        title="🌐 Сайт проекта",
        description="Перейти на pattmsc.online",
        url="https://pattmsc.online/",
        color=discord.Color.blue(),
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="github", description="Ссылка на GitHub проект")
async def github(interaction: discord.Interaction) -> None:
    embed = discord.Embed(
        title="💻 GitHub репозиторий",
        description="faceit-ai-bot на GitHub",
        url="https://github.com/pat1one/faceit-ai-bot",
        color=discord.Color.dark_grey(),
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="links", description="Все основные ссылки проекта")
async def links(interaction: discord.Interaction) -> None:
    embed = discord.Embed(title="🔗 Ссылки проекта", color=discord.Color.purple())
    embed.add_field(
        name="Сайт",
        value="[pattmsc.online](https://pattmsc.online/)",
        inline=False,
    )
    embed.add_field(
        name="GitHub",
        value="[faceit-ai-bot](https://github.com/pat1one/faceit-ai-bot)",
        inline=False,
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="project", description="Краткая информация о проекте")
async def project(interaction: discord.Interaction) -> None:
    embed = discord.Embed(
        title="📦 Faceit AI Bot",
        description="AI‑коуч по демкам и поиск тиммейтов по Faceit",
        color=discord.Color.orange(),
    )
    embed.add_field(
        name="GitHub",
        value="[Репозиторий](https://github.com/pat1one/faceit-ai-bot)",
        inline=False,
    )
    embed.add_field(
        name="Сайт",
        value="[pattmsc.online](https://pattmsc.online/)",
        inline=False,
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="faceit_stats", description="Быстрая статистика игрока по нику Faceit")
@app_commands.describe(nickname="Никнейм на Faceit")
async def faceit_stats(
    interaction: discord.Interaction,
    nickname: str,
) -> None:
    user_key = f"{interaction.user.id}"
    if not await check_bot_rate_limit(
        user_key,
        "faceit_stats",
        limit_per_minute=20,
        limit_per_day=200,
    ):
        await interaction.response.send_message(
            "Превышен лимит запросов для этой команды, попробуй позже.",
            ephemeral=True,
        )
        return
    await interaction.response.defer(thinking=True, ephemeral=True)

    stats = await player_service.get_player_stats(nickname)
    if not stats:
        await interaction.followup.send(
            f"Не удалось найти статистику для **{nickname}**", ephemeral=True
        )
        return

    game_data = stats.get("stats", {}).get("lifetime", {})

    elo = stats.get("elo")
    level = stats.get("level")
    kd_ratio = game_data.get("Average K/D Ratio") or game_data.get("K/D Ratio")
    winrate = game_data.get("Win Rate %")

    embed = discord.Embed(
        title=f"Статистика Faceit: {nickname}",
        color=discord.Color.green(),
    )
    if elo is not None:
        embed.add_field(name="ELO", value=str(elo), inline=True)
    if level is not None:
        embed.add_field(name="Уровень", value=str(level), inline=True)
    if kd_ratio is not None:
        embed.add_field(name="K/D", value=str(kd_ratio), inline=True)
    if winrate is not None:
        embed.add_field(name="Winrate %", value=str(winrate), inline=True)

    await interaction.followup.send(embed=embed, ephemeral=True)


@tree.command(name="tm_find", description="Найти тиммейтов по ELO и языкам")
@app_commands.describe(
    min_elo="Минимальный ELO",
    max_elo="Максимальный ELO",
    language="Язык общения (например, ru или en)",
    role="Желаемая роль (entry/support/igl/any)",
)
async def tm_find(
    interaction: discord.Interaction,
    min_elo: int,
    max_elo: int,
    language: str = "ru",
    role: str = "any",
) -> None:
    user_key = f"{interaction.user.id}"
    if not await check_bot_rate_limit(
        user_key,
        "tm_find",
        limit_per_minute=5,
        limit_per_day=50,
    ):
        await interaction.response.send_message(
            "Превышен лимит запросов для этой команды, попробуй позже.",
            ephemeral=True,
        )
        return

    await interaction.response.defer(thinking=True, ephemeral=True)

    db = SessionLocal()
    try:
        user = User(
            id=0,
            username=f"discord_{interaction.user.id}",
            email=f"discord_{interaction.user.id}@local",
            hashed_password="",
        )

        preferences = TeammatePreferences(
            min_elo=min_elo,
            max_elo=max_elo,
            preferred_maps=[],
            preferred_roles=[] if role == "any" else [role],
            communication_lang=[language],
            play_style="unknown",
            time_zone="unknown",
        )

        profiles = await teammate_service.find_teammates(
            db=db,
            current_user=user,
            preferences=preferences,
        )

        if not profiles:
            await interaction.followup.send(
                "Не удалось найти подходящих тиммейтов с такими параметрами.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title="Найденные тиммейты",
            color=discord.Color.blurple(),
        )

        for p in profiles[:5]:
            score = (
                f"{p.compatibility_score:.1f}"
                if p.compatibility_score is not None
                else "—"
            )
            value_lines = [
                f"ELO: {p.stats.faceit_elo}",
                f"Языки: {', '.join(p.preferences.communication_lang) or '—'}",
                f"Роли: {', '.join(p.preferences.preferred_roles) or '—'}",
                f"Стиль: {p.preferences.play_style}",
            ]
            if p.match_summary:
                value_lines.append("")
                value_lines.append(p.match_summary[:256])

            embed.add_field(
                name=f"{p.faceit_nickname or 'Неизвестный игрок'} (score: {score})",
                value="\n".join(value_lines),
                inline=False,
            )

        await interaction.followup.send(embed=embed, ephemeral=True)
    finally:
        db.close()


@tree.command(name="demo_analyze", description="Анализ CS2 демки (.dem)")
@app_commands.describe(
    demo="Файл демки (.dem)",
    language="Язык отчёта (ru/en)",
)
async def demo_analyze(
    interaction: discord.Interaction,
    demo: discord.Attachment,
    language: str = "ru",
) -> None:
    user_key = f"{interaction.user.id}"
    if not await check_bot_rate_limit(
        user_key,
        "demo_analyze",
        limit_per_minute=3,
        limit_per_day=10,
    ):
        await interaction.response.send_message(
            "Превышен лимит анализов демок для этой команды, попробуй позже.",
            ephemeral=True,
        )
        return

    await interaction.response.defer(thinking=True, ephemeral=True)

    filename = demo.filename or ""
    if not filename.lower().endswith(".dem"):
        await interaction.followup.send(
            "Прикрепи, пожалуйста, файл демки с расширением .dem",
            ephemeral=True,
        )
        return

    if demo.size and demo.size > MAX_DEMO_SIZE_BYTES:
        await interaction.followup.send(
            f"Файл слишком большой. Максимальный размер {MAX_DEMO_SIZE_MB} МБ.",
            ephemeral=True,
        )
        return

    data = await demo.read()
    if not data:
        await interaction.followup.send(
            "Файл пустой, пришли, пожалуйста, валидную демку .dem.",
            ephemeral=True,
        )
        return

    sniff = data[:_SNIFF_BYTES].lower()
    suspicious_markers = (
        b"<html",
        b"<script",
        b"<?php",
        b"#!/bin/bash",
        b"#!/usr/bin/env",
        b"import os",
        b"import sys",
    )
    if any(marker in sniff for marker in suspicious_markers):
        await interaction.followup.send(
            "Похоже, это не бинарная демка CS2. Пришли корректный .dem файл.",
            ephemeral=True,
        )
        return

    file_obj = BytesIO(data)
    upload = UploadFile(filename=filename, file=file_obj)  # type: ignore[arg-type]

    try:
        analysis = await demo_analyzer.analyze_demo(upload, language=language)
    except DemoAnalysisException as exc:
        detail = getattr(exc, "detail", None)
        message = "Не удалось проанализировать демку."
        if isinstance(detail, dict):
            message = str(detail.get("error") or detail) or message
        elif isinstance(detail, str):
            message = detail or message
        await interaction.followup.send(message, ephemeral=True)
        return
    except Exception:
        logger.exception("Discord demo_analyze failed")
        await interaction.followup.send(
            "Произошла внутренняя ошибка при анализе демки.",
            ephemeral=True,
        )
        return

    metadata = analysis.metadata
    coach = analysis.coach_report

    embed = discord.Embed(
        title=f"Анализ демки: {metadata.map_name}",
        description=f"Матч {metadata.match_id} на {metadata.map_name}",
        color=discord.Color.blue(),
    )
    embed.add_field(name="Счёт", value=str(metadata.score), inline=False)

    if coach and coach.summary:
        embed.add_field(
            name="Краткий вывод коуча",
            value=coach.summary[:1024],
            inline=False,
        )
    elif analysis.recommendations:
        joined = "\n".join(analysis.recommendations[:5])
        embed.add_field(
            name="Рекомендации",
            value=joined[:1024],
            inline=False,
        )

    await interaction.followup.send(embed=embed, ephemeral=True)


@tree.command(name="faceit_analyze", description="AI-анализ игрока по нику Faceit")
@app_commands.describe(
    nickname="Никнейм на Faceit",
    language="Язык ответа (ru/en)",
)
async def faceit_analyze(
    interaction: discord.Interaction,
    nickname: str,
    language: str = "ru",
) -> None:
    user_key = f"{interaction.user.id}"
    if not await check_bot_rate_limit(
        user_key,
        "faceit_analyze",
        limit_per_minute=5,
        limit_per_day=50,
    ):
        await interaction.response.send_message(
            "Превышен лимит AI-анализов для этой команды, попробуй позже.",
            ephemeral=True,
        )
        return

    await interaction.response.defer(thinking=True, ephemeral=True)

    analysis = await player_service.analyze_player(nickname, language=language)
    if not analysis:
        await interaction.followup.send(
            f"Не удалось проанализировать игрока **{nickname}**",
            ephemeral=True,
        )
        return

    embed = discord.Embed(
        title=f"AI-анализ игрока: {nickname}",
        color=discord.Color.gold(),
    )

    embed.add_field(
        name="Общий рейтинг",
        value=str(analysis.overall_rating),
        inline=False,
    )

    strengths = analysis.strengths
    weaknesses = analysis.weaknesses

    embed.add_field(
        name="Сильные стороны",
        value=(
            f"Aim: {strengths.aim}\n"
            f"Game sense: {strengths.game_sense}\n"
            f"Positioning: {strengths.positioning}\n"
            f"Teamwork: {strengths.teamwork}\n"
            f"Consistency: {strengths.consistency}"
        ),
        inline=False,
    )

    embed.add_field(
        name="Слабые стороны (priority: " f"{weaknesses.priority})",
        value="\n".join(weaknesses.areas),
        inline=False,
    )

    embed.add_field(
        name="Рекомендации",
        value="\n".join(weaknesses.recommendations),
        inline=False,
    )

    await interaction.followup.send(embed=embed, ephemeral=True)


@client.event
async def on_ready() -> None:
    global GUILD_ID

    try:
        if GUILD_ID is not None:
            guild = discord.Object(id=GUILD_ID)
            tree.copy_global_to(guild=guild)
            synced = await tree.sync(guild=guild)
            logger.info("Синхронизировано %s команд на сервере", len(synced))
        else:
            synced = await tree.sync()
            logger.info("Синхронизировано %s глобальных команд", len(synced))

        logger.info("Discord бот %s запущен", client.user)
    except Exception:
        logger.exception("Ошибка при синхронизации команд Discord")


def main() -> None:
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_BOT_TOKEN не задан в переменных окружения")

    client.run(token)


if __name__ == "__main__":
    main()
