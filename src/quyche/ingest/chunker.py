"""Chia văn bản quy chế thành các Điều.

PHẦN LÕI BẠN TỰ VIẾT, tuần 1. Test: tests/test_chunker.py (xóa marker `todo` khi xong).

Văn bản quy phạm ở Việt Nam có cấu trúc: Chương → Điều → Khoản ("1.", "2.") → Điểm ("a)", "b)").
Một Điều thường trả lời trọn một ý ("Điều kiện tốt nghiệp", "Học phí"), nên đó là đơn vị chunk
tự nhiên hơn nhiều so với cắt cố định N ký tự.
"""

from __future__ import annotations

from quyche.schemas import Chunk

TODO_HINT = "Tuần 1: tự cài đặt hàm này, xem ROADMAP.md và tests/test_chunker.py"


def split_into_articles(text: str, doc_id: str) -> list[Chunk]:
    """Chia text (đã qua ``normalize_text``) thành danh sách Chunk, mỗi Chunk là một Điều.

    Yêu cầu:
    - Một Điều bắt đầu ở ĐẦU DÒNG bằng "Điều <số>." (số có thể kèm chữ thường: "Điều 12a."),
      tiêu đề nằm cùng dòng: "Điều 12. Học phí".
    - ``article`` là số điều dạng chuỗi ("12", "12a"); ``article_title`` là tiêu đề ("Học phí").
    - ``text`` là toàn bộ nội dung của Điều, gồm cả dòng tiêu đề.
    - ``chunk_id = f"{doc_id}:dieu-{article}"``, ``clause = None``.
    - Phần trước Điều đầu tiên (quốc hiệu, "Căn cứ...", "Chương I") bị bỏ qua.
    - Dòng "Chương II" / "CHƯƠNG II" và dòng tên chương ngay sau nó KHÔNG được dính vào
      cuối Điều đứng trước.
    - "Điều" nằm giữa câu, hoặc ở đầu dòng do xuống dòng nhưng không có dấu chấm ngay sau số
      (ví dụ "Điều 3 của quy chế này."), KHÔNG phải Điều mới.
    - Text rỗng thì trả về ``[]``.

    Gợi ý: ``re.compile(r"^...$", re.MULTILINE)``; ``re.finditer`` cho vị trí bắt đầu
    của từng Điều.
    """
    raise NotImplementedError(TODO_HINT)
