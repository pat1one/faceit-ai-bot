# 📚 Faceit AI Bot Documentation (EN)

**Language:** [Русский](./index.md) | English

## 🌐 Main Site

✅ **Production site:** [pattmsc.online](https://pattmsc.online)

## 📚 Documentation

✅ **Documentation on GitHub Pages:** <https://pat1one.github.io/faceit-ai-bot/>

## 📋 Project Overview

Faceit AI Bot is a tool for analyzing CS2 player statistics on the Faceit platform. It helps you:

- find compatible teammates,
- analyze demos,
- and improve your gameplay using detailed stats and AI-driven recommendations.

## 🚀 Production Deployment

- 🌐 **VPS hosting:** Ubuntu 24.04
- 🔒 **SSL certificate:** Let's Encrypt
- 🚀 **Reverse proxy:** Nginx with basic optimizations
- 🐳 **Containers:** Docker for all services (API, web, bots, DB, cache)
- 🔄 **CI/CD:** GitHub Actions automation

## ✨ Key Features

🤖 **AI / Analytics**
- 🧠 Groq-powered insights for CS2 gameplay
- 🤖 AI analysis of player stats with recommendations
- 📊 Historical analytics to track progress

📈 **Stats & Data**
- 📊 Faceit API integration for live data
- 🗄️ PostgreSQL for analytics storage
- 📈 Demo analysis with key rounds and situations
- 👥 Teammate finder with AI-enriched matching
- 💡 Personalized training plan suggestions
- 📱 PWA support (install as an app)

🔐 **Security & Integrations**
- 🔐 CAPTCHA protection for login/registration/payments
  (Cloudflare Turnstile + Yandex SmartCaptcha for Russian users)
- 🤖 Telegram/Discord bots for quick checks and demos

> Disclaimer: Discord is blocked in some regions (including Russia). Use at your own risk. The integration is shown mainly for educational/demo purposes.

## 🛠️ Tech Stack (Short)

- **Backend:** Python, FastAPI, PostgreSQL, Redis
- **AI:** Groq, LangChain, optional local LLM via OpenAI-compatible API
- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **DevOps:** Docker, GitHub Actions, Nginx

## 🚀 Quick Start

1. Visit [pattmsc.online](https://pattmsc.online)
2. Enter a Faceit nickname
3. Get a detailed analysis and recommendations

## 📖 More

- 📦 [Releases](https://github.com/pat1one/faceit-ai-bot/releases)
- 🐛 [Bug reports](https://github.com/pat1one/faceit-ai-bot/issues)
- 💡 [Feature ideas](https://github.com/pat1one/faceit-ai-bot/issues/new?template=feature_request.md)
- 🤝 [Contributing](https://github.com/pat1one/faceit-ai-bot/blob/main/CONTRIBUTING.md)

## 📄 License

This project is distributed under a custom **source-available** license.
See the full terms in [LICENSE](https://github.com/pat1one/faceit-ai-bot/blob/main/LICENSE).

---
**⭐ If you like the project, please star it on GitHub!**
