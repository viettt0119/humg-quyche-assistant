"""Kiểm tra kiểu dữ liệu và đọc/ghi JSONL (hạ tầng, pass ngay)."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from quyche.jsonl import read_jsonl, write_jsonl
from quyche.schemas import Chunk, EvalQuestion, GoldRef, ref_key


def test_chunk_and_gold_share_the_same_key():
    c = Chunk(chunk_id="qc:dieu-12", doc_id="qc", article="12", text="Điều 12. Học phí")
    assert c.ref_key == GoldRef(doc_id="qc", article="12").key == ref_key("qc", "12")


def test_question_split_is_validated():
    with pytest.raises(ValidationError):
        EvalQuestion(qid="q1", question="?", split="train")


def test_unanswerable_question():
    q = EvalQuestion(qid="q1", question="Ký túc xá giá bao nhiêu?", split="dev")
    assert not q.answerable


def test_jsonl_roundtrip_keeps_vietnamese(tmp_path):
    path = tmp_path / "sub" / "chunks.jsonl"
    items = [
        Chunk(chunk_id="qc:dieu-1", doc_id="qc", article="1", text="Điều 1. Phạm vi điều chỉnh"),
        Chunk(chunk_id="qc:dieu-2", doc_id="qc", article="2", text="Điều 2. Giải thích từ ngữ"),
    ]
    assert write_jsonl(path, items) == 2
    assert read_jsonl(path, Chunk) == items


def test_jsonl_reports_bad_line(tmp_path):
    path = tmp_path / "bad.jsonl"
    path.write_text('{"qid": "q1"}\n', encoding="utf-8")
    with pytest.raises(ValueError, match=r"bad\.jsonl:1"):
        read_jsonl(path, EvalQuestion)


def test_example_questions_file_is_valid():
    path = Path(__file__).parents[1] / "eval" / "questions.jsonl"
    questions = read_jsonl(path, EvalQuestion)
    assert questions, "eval/questions.jsonl không được rỗng"
