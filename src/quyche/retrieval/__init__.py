"""Đăng ký các bộ truy xuất theo tên để CLI và runner gọi được.

Khi viết bộ truy xuất mới (vector ở tuần 3, hybrid...), thêm nó vào ``REGISTRY``.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

from quyche.retrieval.base import Retriever
from quyche.retrieval.bm25 import BM25Retriever
from quyche.schemas import Chunk

REGISTRY: dict[str, Callable[[Sequence[Chunk]], Retriever]] = {
    "bm25": BM25Retriever,
}


def build_retriever(name: str, chunks: Sequence[Chunk]) -> Retriever:
    try:
        factory = REGISTRY[name]
    except KeyError:
        options = ", ".join(sorted(REGISTRY))
        raise ValueError(f"Không có retriever '{name}'. Các lựa chọn: {options}") from None
    return factory(chunks)


__all__ = ["REGISTRY", "Retriever", "build_retriever"]
