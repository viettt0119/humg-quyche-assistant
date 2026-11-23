"""Metric đánh giá truy xuất.

PHẦN LÕI BẠN TỰ VIẾT, tuần 2. Test: tests/test_metrics.py (xóa marker `todo` khi xong).

Cả hai hàm làm việc trên KHÓA (``ref_key`` dạng "doc_id#article"), không phải chunk:
- ``retrieved``: khóa của các kết quả theo đúng thứ tự trả về. Có thể lặp lại, vì một Điều
  có thể bị chia thành nhiều chunk.
- ``relevant``: tập khóa đúng của câu hỏi (không rỗng).
"""

from __future__ import annotations

from collections.abc import Sequence

TODO_HINT = "Tuần 2: tự cài đặt metric này, xem ROADMAP.md và tests/test_metrics.py"


def recall_at_k(retrieved: Sequence[str], relevant: set[str], k: int) -> float:
    """Tỉ lệ khóa trong ``relevant`` xuất hiện trong ``k`` kết quả đầu tiên.

    Khóa lặp lại chỉ được tính một lần. ``relevant`` rỗng thì raise ``ValueError``
    (câu hỏi không có đáp án phải được lọc ra trước khi tính).
    """
    raise NotImplementedError(TODO_HINT)


def reciprocal_rank(retrieved: Sequence[str], relevant: set[str], k: int = 10) -> float:
    """1 / (thứ hạng của kết quả đúng đầu tiên trong ``k`` kết quả đầu), hoặc 0 nếu không có.

    Thứ hạng bắt đầu từ 1. MRR là trung bình của giá trị này trên mọi câu hỏi.
    ``relevant`` rỗng thì raise ``ValueError``.
    """
    raise NotImplementedError(TODO_HINT)
