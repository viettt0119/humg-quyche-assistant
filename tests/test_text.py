"""Tuần 1: normalize_text và tokenize. Xóa dòng `pytestmark` khi bạn cài đặt xong."""

import unicodedata

import pytest

from quyche.text import normalize_text, tokenize

pytestmark = pytest.mark.todo


def nfd(s: str) -> str:
    return unicodedata.normalize("NFD", s)


class TestNormalizeText:
    def test_converts_decomposed_diacritics_to_nfc(self):
        raw = nfd("Điều kiện tốt nghiệp")
        assert raw != "Điều kiện tốt nghiệp"  # trông giống nhưng khác nhau từng code point
        assert normalize_text(raw) == "Điều kiện tốt nghiệp"

    def test_collapses_spaces_tabs_and_nbsp(self):
        assert normalize_text("Học  phí \t năm   học") == "Học phí năm học"

    def test_strips_each_line(self):
        assert normalize_text("  Điều 1. Phạm vi  \n   1. Nội dung ") == (
            "Điều 1. Phạm vi\n1. Nội dung"
        )

    def test_keeps_line_breaks_but_collapses_blank_lines(self):
        assert normalize_text("Chương I\n\n\n\nĐiều 1. Phạm vi") == "Chương I\n\nĐiều 1. Phạm vi"

    def test_lines_with_only_spaces_count_as_blank(self):
        assert normalize_text("a\n   \n \t \nb") == "a\n\nb"

    def test_strips_whole_text(self):
        assert normalize_text("\n\n  Điều 1. A  \n\n") == "Điều 1. A"


class TestTokenize:
    def test_lowercases_and_drops_punctuation(self):
        assert tokenize("Điều 12. Học phí (năm 2021)!") == [
            "điều",
            "12",
            "học",
            "phí",
            "năm",
            "2021",
        ]

    def test_keeps_vietnamese_diacritics(self):
        assert tokenize("học") != tokenize("hoc")

    def test_normalizes_unicode_itself(self):
        assert tokenize(nfd("Học phí")) == ["học", "phí"]

    def test_empty_and_punctuation_only(self):
        assert tokenize("") == []
        assert tokenize(" ... ;; !! ") == []
