"""Đọc và ghi file JSON Lines (mỗi dòng một object)."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from pydantic import BaseModel


def write_jsonl[M: BaseModel](path: Path, items: Iterable[M]) -> int:
    """Ghi từng model thành một dòng JSON. Trả về số dòng đã ghi."""
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(item.model_dump_json() + "\n")
            count += 1
    return count


def read_jsonl[M: BaseModel](path: Path, model: type[M]) -> list[M]:
    """Đọc file JSONL thành danh sách model. Bỏ qua dòng trống."""
    items: list[M] = []
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                items.append(model.model_validate_json(line))
            except ValueError as e:
                raise ValueError(f"{path}:{line_no}: dòng không hợp lệ: {e}") from e
    return items
