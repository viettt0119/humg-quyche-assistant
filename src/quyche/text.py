"""Chuẩn hóa và tách token văn bản tiếng Việt.

PHẦN LÕI BẠN TỰ VIẾT, tuần 1. Test: tests/test_text.py (xóa marker `todo` khi xong).
"""

from __future__ import annotations

TODO_HINT = "Tuần 1: tự cài đặt hàm này, xem ROADMAP.md và tests/test_text.py"


def normalize_text(text: str) -> str:
    """Chuẩn hóa text lấy từ PDF trước khi chia chunk.

    Yêu cầu:
    1. Đưa về chuẩn Unicode NFC. PDF tiếng Việt hay trả về dạng tổ hợp (NFD), ví dụ "ế"
       thành "e" + dấu mũ + dấu sắc. Hai chuỗi trông giống hệt nhau nhưng ``==`` trả False,
       và tìm kiếm sẽ hỏng âm thầm.
    2. Thay khoảng trắng đặc biệt (NBSP ``\\u00a0``, tab) bằng dấu cách thường.
    3. Trong mỗi dòng: gộp nhiều dấu cách liền nhau thành một, bỏ khoảng trắng đầu và cuối dòng.
    4. Giữ xuống dòng (chunker cần nó để nhận ra "Điều X."), nhưng nhiều dòng trống liên tiếp
       gộp lại thành đúng một dòng trống.
    5. Bỏ khoảng trắng và dòng trống ở đầu và cuối toàn văn bản.

    Gợi ý: module ``unicodedata`` và ``re`` trong thư viện chuẩn là đủ.
    """
    raise NotImplementedError(TODO_HINT)


def tokenize(text: str) -> list[str]:
    """Tách text thành token mức âm tiết, dùng cho BM25.

    Yêu cầu:
    - Tự chuẩn hóa NFC trước (đầu vào có thể là câu hỏi người dùng gõ, chưa qua normalize_text).
    - Chuyển về chữ thường.
    - Bỏ dấu câu và ký hiệu; giữ chữ và số ("2021", "15").
    - GIỮ dấu tiếng Việt: "học" và "hoc" là hai token khác nhau.

    Ở tuần 2 bạn sẽ thử thêm tách từ ("học phí" thành một token) bằng pyvi hoặc underthesea
    và so sánh (thí nghiệm E2). Khi đó có thể thêm tham số, nhưng giữ hành vi mặc định này.
    """
    raise NotImplementedError(TODO_HINT)
