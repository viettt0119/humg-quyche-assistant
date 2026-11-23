"""Kiểu dữ liệu dùng chung giữa các bước ingest, truy xuất và đánh giá."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


def ref_key(doc_id: str, article: str) -> str:
    """Khóa định danh một Điều trong một văn bản, ví dụ ``"quy-che-dao-tao-2021#12"``.

    Dùng để so khớp kết quả truy xuất với đáp án đúng trong bộ đánh giá.
    """
    return f"{doc_id}#{article}"


class Document(BaseModel):
    """Một văn bản quy chế đã được trích text từ PDF."""

    doc_id: str = Field(description="Tên file PDF không có đuôi, ví dụ 'quy-che-dao-tao-2021'")
    source_path: str
    pages: list[str] = Field(description="Text của từng trang, chưa chuẩn hóa")


class Chunk(BaseModel):
    """Một đơn vị để tìm kiếm. Hiện tại: một Điều. Có thể chia nhỏ tới Khoản ở các tuần sau."""

    chunk_id: str
    doc_id: str
    article: str = Field(description="Số điều dạng chuỗi: '12', '12a'")
    article_title: str = ""
    clause: str | None = Field(default=None, description="Số khoản nếu chia tới Khoản")
    text: str

    @property
    def ref_key(self) -> str:
        return ref_key(self.doc_id, self.article)


class GoldRef(BaseModel):
    """Một Điều cần có để trả lời đúng câu hỏi."""

    doc_id: str
    article: str

    @property
    def key(self) -> str:
        return ref_key(self.doc_id, self.article)


class EvalQuestion(BaseModel):
    """Một câu hỏi trong bộ đánh giá ``eval/questions.jsonl``."""

    qid: str
    question: str
    gold: list[GoldRef] = Field(
        default_factory=list,
        description="Các Điều trả lời được câu hỏi. Để trống nếu dữ liệu không có đáp án",
    )
    split: Literal["dev", "test"]
    source: Literal["form", "log", "self"] = "form"
    example: bool = Field(
        default=False, description="Câu ví dụ trong khung repo, bị bỏ qua khi chạy"
    )
    notes: str = ""

    @property
    def answerable(self) -> bool:
        return bool(self.gold)


class SearchHit(BaseModel):
    """Một kết quả truy xuất."""

    chunk: Chunk
    score: float
    rank: int = Field(ge=1, description="Thứ hạng, bắt đầu từ 1")
