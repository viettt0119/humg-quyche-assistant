"""Giao diện chung cho mọi bộ truy xuất (BM25, vector, hybrid...)."""

from __future__ import annotations

from typing import Protocol

from quyche.schemas import SearchHit


class Retriever(Protocol):
    name: str

    def search(self, query: str, k: int = 5) -> list[SearchHit]:
        """Trả về tối đa ``k`` kết quả, sắp xếp theo điểm giảm dần, ``rank`` bắt đầu từ 1."""
        ...
