"""Tuần 2: BM25Retriever. Xóa dòng `pytestmark` khi bạn cài đặt xong.

Cần `tokenize` (tuần 1) chạy đúng trước. Giá trị kỳ vọng tính tay theo đúng công thức
trong docstring của quyche/retrieval/bm25.py (k1 = 1.5, b = 0.75).
"""

import pytest

from quyche.retrieval.bm25 import BM25Retriever
from quyche.schemas import Chunk

pytestmark = pytest.mark.todo


def chunk(article: str, text: str) -> Chunk:
    return Chunk(chunk_id=f"t:dieu-{article}", doc_id="t", article=article, text=text)


@pytest.fixture
def retriever():
    return BM25Retriever(
        [
            chunk("1", "học phí tín chỉ"),
            chunk("2", "điều kiện tốt nghiệp"),
            chunk("3", "học bổng khuyến khích học tập"),
        ]
    )


def test_most_relevant_first(retriever):
    hits = retriever.search("học phí", k=3)
    assert hits[0].chunk.article == "1"


def test_exact_scores(retriever):
    scores = {h.chunk.article: h.score for h in retriever.search("học", k=3)}
    # Chunk 3 có "học" hai lần nên thắng, dù dài hơn chunk 1: thấy được TF và chuẩn hóa độ dài.
    assert scores == {
        "3": pytest.approx(0.614958, rel=1e-4),
        "1": pytest.approx(0.502294, rel=1e-4),
    }


def test_ranks_sorted_and_limited(retriever):
    hits = retriever.search("học phí", k=1)
    assert len(hits) == 1
    hits = retriever.search("học phí", k=3)
    assert [h.rank for h in hits] == list(range(1, len(hits) + 1))
    assert [h.score for h in hits] == sorted((h.score for h in hits), reverse=True)


def test_only_positive_scores(retriever):
    assert [h.chunk.article for h in retriever.search("tốt nghiệp", k=3)] == ["2"]


def test_no_match_returns_empty(retriever):
    assert retriever.search("ký túc xá", k=3) == []


def test_repeated_query_terms_count_once(retriever):
    once = retriever.search("học", k=3)
    twice = retriever.search("học học", k=3)
    assert [h.score for h in once] == pytest.approx([h.score for h in twice])


def test_query_is_case_and_unicode_insensitive(retriever):
    assert retriever.search("HỌC PHÍ", k=1)[0].chunk.article == "1"
