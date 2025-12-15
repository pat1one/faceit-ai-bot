from datetime import datetime
from pathlib import Path

import json

from src.server.features.demo_analyzer.models import (
    CoachReport,
    DemoAnalysisInput,
    DemoTrainingSample,
)
from ml.prepare_demo_coach_data import (
    build_completion,
    build_prompt,
    prepare_dataset,
)


def _make_sample(language: str = "ru") -> DemoTrainingSample:
    demo_input = DemoAnalysisInput(
        language=language,
        player={"id": "p1"},
        match={"id": "m1"},
        aggregate_stats={"kills": 10},
        flags=["test"],
        key_rounds=[{"round": 1}],
    )

    report = CoachReport(
        overview="overview",
        strengths=[{"area": "aim"}],
        weaknesses=[{"area": "positioning"}],
        key_moments=[{"round": 1}],
        training_plan=[{"task": "dm"}],
        summary="summary",
    )

    return DemoTrainingSample(
        input=demo_input,
        output=report,
        source="unit_test",
        created_at=datetime(2025, 1, 1, 12, 0, 0),
    )


def test_build_prompt_includes_header_and_json_ru() -> None:
    sample = _make_sample(language="ru")

    prompt = build_prompt(sample)

    assert "Ты — AI‑тренер по CS2" in prompt
    assert "\n\nВходные данные:\n" in prompt

    # JSON part should contain language and player fields
    assert '"language": "ru"' in prompt
    assert '"player"' in prompt


def test_build_prompt_includes_header_and_json_en() -> None:
    sample = _make_sample(language="en")

    prompt = build_prompt(sample)

    assert "You are an AI CS2 coach" in prompt
    assert "\n\nInput data:\n" in prompt
    assert '"language": "en"' in prompt


def test_build_completion_serializes_coach_report() -> None:
    sample = _make_sample(language="ru")

    completion = build_completion(sample)

    data = json.loads(completion)
    assert data["overview"] == "overview"
    assert isinstance(data.get("strengths"), list)
    assert isinstance(data.get("weaknesses"), list)


def test_prepare_dataset_reads_samples_and_writes_prompt_completion(tmp_path: Path) -> None:
    input_path = tmp_path / "samples.jsonl"
    output_path = tmp_path / "prepared.jsonl"

    sample = _make_sample(language="ru")
    bad_line = "this is not json"

    with input_path.open("w", encoding="utf-8") as f:
        # Valid sample
        f.write(sample.model_dump_json(ensure_ascii=False) + "\n")
        # Empty line should be skipped
        f.write("\n")
        # Invalid JSON line should be skipped with an error message
        f.write(bad_line + "\n")

    prepare_dataset(input_path, output_path)

    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1

    record = json.loads(lines[0])
    assert record["language"] == "ru"
    assert record["source"] == "unit_test"
    assert "prompt" in record
    assert "completion" in record
    # created_at is serialized as ISO string
    assert record["created_at"].startswith("2025-01-01T12:00:00")
