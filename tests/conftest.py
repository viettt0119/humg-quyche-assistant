"""Nhắc số test TODO còn lại sau mỗi lần chạy pytest."""

from __future__ import annotations

from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"
_todo = {"deselected": 0}


@pytest.fixture
def sample_regulation() -> str:
    return (FIXTURES / "sample_regulation.txt").read_text(encoding="utf-8")


def pytest_deselected(items: list[pytest.Item]) -> None:
    _todo["deselected"] += sum(1 for item in items if item.get_closest_marker("todo"))


def pytest_terminal_summary(terminalreporter: pytest.TerminalReporter) -> None:
    if _todo["deselected"]:
        terminalreporter.write_line(
            f"Còn {_todo['deselected']} test TODO cho phần lõi bạn tự viết. "
            "Xem chi tiết: uv run pytest -m todo",
            yellow=True,
        )
