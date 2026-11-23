"""Tuần 2: recall_at_k và reciprocal_rank. Xóa dòng `pytestmark` khi bạn cài đặt xong."""

import pytest

from quyche.evaluation.metrics import recall_at_k, reciprocal_rank

pytestmark = pytest.mark.todo


class TestRecallAtK:
    def test_partial(self):
        assert recall_at_k(["a", "b", "c"], {"b", "x"}, k=2) == pytest.approx(0.5)

    def test_cutoff_matters(self):
        assert recall_at_k(["a", "b", "c"], {"c"}, k=2) == 0.0
        assert recall_at_k(["a", "b", "c"], {"c"}, k=3) == 1.0

    def test_duplicates_count_once(self):
        assert recall_at_k(["b", "b", "c"], {"b", "c"}, k=2) == pytest.approx(0.5)

    def test_k_larger_than_results(self):
        assert recall_at_k(["a"], {"a", "b"}, k=10) == pytest.approx(0.5)

    def test_empty_retrieved(self):
        assert recall_at_k([], {"a"}, k=5) == 0.0

    def test_empty_relevant_is_an_error(self):
        with pytest.raises(ValueError):
            recall_at_k(["a"], set(), k=5)


class TestReciprocalRank:
    def test_first_hit_rank(self):
        assert reciprocal_rank(["a", "b", "c"], {"c", "b"}) == pytest.approx(1 / 2)

    def test_top_hit(self):
        assert reciprocal_rank(["a"], {"a"}) == 1.0

    def test_no_hit(self):
        assert reciprocal_rank(["a", "b"], {"z"}) == 0.0

    def test_cutoff(self):
        assert reciprocal_rank(["a", "b", "c"], {"c"}, k=2) == 0.0

    def test_empty_relevant_is_an_error(self):
        with pytest.raises(ValueError):
            reciprocal_rank(["a"], set())
