"""Okapi BM25 tự cài đặt.

PHẦN LÕI BẠN TỰ VIẾT, tuần 2. Test: tests/test_bm25.py (xóa marker `todo` khi xong).

Công thức (dùng đúng công thức này để khớp test):

    score(D, Q) = Σ_{t ∈ Q} IDF(t) · f(t, D) · (k1 + 1) / (f(t, D) + k1 · (1 − b + b · |D| / avgdl))
    IDF(t)      = ln( (N − n(t) + 0.5) / (n(t) + 0.5) + 1 )

- f(t, D): số lần token t xuất hiện trong chunk D
- |D|: số token của D; avgdl: số token trung bình của mọi chunk
- N: số chunk; n(t): số chunk có chứa t
- Q được tách token bằng ``tokenize``. Token lặp lại trong câu hỏi chỉ tính một lần.

Sau khi tự viết xong, so kết quả với thư viện ``rank-bm25`` để kiểm tra chéo
(ghi vào EXPERIMENTS.md).
"""

from __future__ import annotations

from collections.abc import Sequence

from quyche.schemas import Chunk, SearchHit

TODO_HINT = "Tuần 2: tự cài đặt BM25, xem ROADMAP.md và tests/test_bm25.py"


class BM25Retriever:
    name = "bm25"

    def __init__(self, chunks: Sequence[Chunk], k1: float = 1.5, b: float = 0.75) -> None:
        """Lập chỉ mục cho ``chunk.text`` của từng chunk (tách token bằng ``quyche.text.tokenize``).

        Tính sẵn mọi thứ không phụ thuộc câu hỏi: tần suất token mỗi chunk, độ dài, avgdl, IDF.
        """
        raise NotImplementedError(TODO_HINT)

    def search(self, query: str, k: int = 5) -> list[SearchHit]:
        """Trả về tối đa ``k`` chunk có điểm > 0, điểm giảm dần, ``rank`` bắt đầu từ 1.

        Không có token nào khớp thì trả về ``[]``.
        """
        raise NotImplementedError(TODO_HINT)
