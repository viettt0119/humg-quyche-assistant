"""Tuần 1: split_into_articles. Xóa dòng `pytestmark` khi bạn cài đặt xong.

Dữ liệu: tests/fixtures/sample_regulation.txt, văn bản mẫu tự tạo theo đúng format
Chương/Điều/Khoản.
Khi gặp trường hợp khó trong PDF thật, hãy thêm vào fixture và viết thêm test.
"""

import pytest

from quyche.ingest.chunker import split_into_articles

pytestmark = pytest.mark.todo

DOC = "mau"


@pytest.fixture
def chunks(sample_regulation):
    return split_into_articles(sample_regulation, DOC)


def by_article(chunks):
    return {c.article: c for c in chunks}


def test_finds_every_article_in_order(chunks):
    assert [c.article for c in chunks] == ["1", "2", "3", "3a", "4"]


def test_extracts_titles(chunks):
    assert [c.article_title for c in chunks] == [
        "Phạm vi điều chỉnh",
        "Giải thích từ ngữ",
        "Mức học phí",
        "Miễn, giảm học phí",
        "Điều kiện tốt nghiệp",
    ]


def test_ids_and_doc(chunks):
    for c in chunks:
        assert c.doc_id == DOC
        assert c.chunk_id == f"{DOC}:dieu-{c.article}"
        assert c.clause is None


def test_text_starts_with_heading_and_keeps_body(chunks):
    a = by_article(chunks)
    for c in chunks:
        assert c.text.startswith(f"Điều {c.article}.")
    assert "2. Sinh viên nộp học phí trước ngày bắt đầu học kỳ." in a["3"].text
    assert a["4"].text.rstrip().endswith("đạt từ 2,0 trở lên.")


def test_skips_preamble(chunks):
    assert not any("Căn cứ" in c.text for c in chunks)
    assert not any("QUY CHẾ MẪU" in c.text for c in chunks)


def test_chapter_headings_not_glued_to_previous_article(chunks):
    a = by_article(chunks)
    assert "Chương II" not in a["2"].text
    assert "HỌC PHÍ" not in a["2"].text
    assert "CHƯƠNG III" not in a["3a"].text
    assert "TỐT NGHIỆP" not in a["3a"].text


def test_inline_and_wrapped_references_are_not_new_articles(chunks):
    a = by_article(chunks)
    # "Điều 3" đứng đầu dòng do xuống dòng, không có dấu chấm sau số: vẫn thuộc Điều 2.
    assert "Điều 3 của quy chế này." in a["2"].text
    assert "theo quy định tại Điều 3." in a["3a"].text


def test_empty_text():
    assert split_into_articles("", DOC) == []
