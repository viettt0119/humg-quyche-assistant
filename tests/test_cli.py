"""Kiểm tra CLI và runner (hạ tầng). Dùng retriever giả nên không phụ thuộc phần lõi."""

from collections.abc import Sequence

import pytest
from typer.testing import CliRunner

from quyche import retrieval
from quyche.cli import app
from quyche.evaluation.runner import evaluate, load_questions
from quyche.jsonl import write_jsonl
from quyche.schemas import Chunk, EvalQuestion, GoldRef, SearchHit

runner = CliRunner()

CHUNKS = [
    Chunk(chunk_id="qc:dieu-3", doc_id="qc", article="3", article_title="Mức học phí", text="x"),
    Chunk(chunk_id="qc:dieu-4", doc_id="qc", article="4", article_title="Tốt nghiệp", text="y"),
]


class FakeRetriever:
    """Luôn trả về các chunk theo thứ tự cố định."""

    name = "fake"

    def __init__(self, chunks: Sequence[Chunk]) -> None:
        self.chunks = list(chunks)

    def search(self, query: str, k: int = 5) -> list[SearchHit]:
        return [
            SearchHit(chunk=c, score=1.0 / (i + 1), rank=i + 1)
            for i, c in enumerate(self.chunks[:k])
        ]


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    monkeypatch.setenv("QUYCHE_RAW_DIR", str(tmp_path / "raw"))
    monkeypatch.setenv("QUYCHE_CHUNKS_PATH", str(tmp_path / "chunks.jsonl"))
    monkeypatch.setenv("QUYCHE_QUESTIONS_PATH", str(tmp_path / "questions.jsonl"))
    monkeypatch.setenv("QUYCHE_REPORTS_DIR", str(tmp_path / "reports"))
    monkeypatch.setitem(retrieval.REGISTRY, "fake", FakeRetriever)
    return tmp_path


def test_ingest_without_pdfs_explains_what_to_do(workspace):
    result = runner.invoke(app, ["ingest"])
    assert result.exit_code == 1
    assert "Chưa có PDF" in result.output


def test_search_without_chunks_explains_what_to_do(workspace):
    result = runner.invoke(app, ["search", "học phí"])
    assert result.exit_code == 1
    assert "quyche ingest" in result.output


def test_search_prints_hits(workspace):
    write_jsonl(workspace / "chunks.jsonl", CHUNKS)
    result = runner.invoke(app, ["search", "học phí", "-r", "fake", "-k", "1"])
    assert result.exit_code == 0, result.output
    assert "Điều 3" in result.output
    assert "Điều 4" not in result.output


def test_unknown_retriever(workspace):
    write_jsonl(workspace / "chunks.jsonl", CHUNKS)
    result = runner.invoke(app, ["search", "học phí", "-r", "khong-co"])
    assert result.exit_code == 1
    assert "bm25" in result.output


def test_test_split_needs_confirmation(workspace):
    result = runner.invoke(app, ["eval", "--split", "test"])
    assert result.exit_code == 1
    assert "--confirm-test" in result.output


def test_eval_ignores_example_questions(workspace):
    write_jsonl(workspace / "chunks.jsonl", CHUNKS)
    write_jsonl(
        workspace / "questions.jsonl",
        [EvalQuestion(qid="ex", question="?", split="dev", example=True)],
    )
    result = runner.invoke(app, ["eval", "-r", "fake"])
    assert result.exit_code == 1
    assert "Chưa có câu hỏi thật" in result.output


def test_load_questions_filters_split_and_examples(tmp_path):
    path = tmp_path / "q.jsonl"
    write_jsonl(
        path,
        [
            EvalQuestion(qid="d1", question="a", split="dev"),
            EvalQuestion(qid="t1", question="b", split="test"),
            EvalQuestion(qid="ex", question="c", split="dev", example=True),
        ],
    )
    assert [q.qid for q in load_questions(path, "dev")] == ["d1"]


def test_evaluate_needs_at_least_one_answerable_question():
    questions = [EvalQuestion(qid="u1", question="Ký túc xá?", split="dev")]
    with pytest.raises(ValueError, match="có đáp án"):
        evaluate(FakeRetriever(CHUNKS), questions)


@pytest.mark.todo
def test_eval_end_to_end(workspace):
    """Pass khi metrics (tuần 2) đã viết xong. Retriever giả xếp Điều 3 đứng đầu, Điều 4 thứ hai."""
    write_jsonl(workspace / "chunks.jsonl", CHUNKS)
    write_jsonl(
        workspace / "questions.jsonl",
        [
            EvalQuestion(
                qid="q1", question="a", split="dev", gold=[GoldRef(doc_id="qc", article="3")]
            ),
            EvalQuestion(
                qid="q2", question="b", split="dev", gold=[GoldRef(doc_id="qc", article="4")]
            ),
            EvalQuestion(qid="q3", question="c", split="dev"),
        ],
    )
    result = runner.invoke(app, ["eval", "-r", "fake"])
    assert result.exit_code == 0, result.output
    assert "recall@1" in result.output
    assert "Bỏ qua 1 câu" in result.output
    report = next((workspace / "reports").glob("*-fake-dev.json")).read_text(encoding="utf-8")
    assert '"recall@1": 0.5' in report
    assert '"mrr@10": 0.75' in report
