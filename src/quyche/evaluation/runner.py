"""Chạy bộ đánh giá: câu hỏi → retriever → metric → báo cáo.

File này là hạ tầng, viết sẵn. Nó gọi các metric bạn tự viết trong ``metrics.py``.
"""

from __future__ import annotations

import statistics
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter

from pydantic import BaseModel

from quyche.evaluation.metrics import recall_at_k, reciprocal_rank
from quyche.jsonl import read_jsonl
from quyche.retrieval.base import Retriever
from quyche.schemas import EvalQuestion

DEFAULT_KS: tuple[int, ...] = (1, 3, 5, 10)


class QuestionResult(BaseModel):
    qid: str
    question: str
    gold: list[str]
    retrieved: list[str]
    recall: dict[str, float]
    reciprocal_rank: float
    latency_ms: float


class EvalReport(BaseModel):
    retriever: str
    split: str
    created_at: datetime
    n_questions: int
    n_unanswerable_skipped: int
    metrics: dict[str, float]
    mean_latency_ms: float
    results: list[QuestionResult]


def load_questions(path: Path, split: str) -> list[EvalQuestion]:
    """Câu hỏi thuộc ``split``, đã bỏ các câu ví dụ (``example: true``)."""
    return [q for q in read_jsonl(path, EvalQuestion) if q.split == split and not q.example]


def evaluate(
    retriever: Retriever,
    questions: Sequence[EvalQuestion],
    ks: Sequence[int] = DEFAULT_KS,
    split: str = "dev",
) -> EvalReport:
    """Đo Recall@k và MRR trên các câu hỏi có đáp án. Câu không có đáp án được đếm và bỏ qua."""
    max_k = max(ks)
    results: list[QuestionResult] = []
    skipped = 0
    for q in questions:
        if not q.answerable:
            skipped += 1
            continue
        start = perf_counter()
        hits = retriever.search(q.question, k=max_k)
        latency_ms = (perf_counter() - start) * 1000
        retrieved = [h.chunk.ref_key for h in hits]
        relevant = {g.key for g in q.gold}
        results.append(
            QuestionResult(
                qid=q.qid,
                question=q.question,
                gold=sorted(relevant),
                retrieved=retrieved,
                recall={f"recall@{k}": recall_at_k(retrieved, relevant, k) for k in ks},
                reciprocal_rank=reciprocal_rank(retrieved, relevant, k=max_k),
                latency_ms=round(latency_ms, 2),
            )
        )
    if not results:
        raise ValueError(f"Không có câu hỏi nào có đáp án trong split '{split}'.")

    metrics = {
        f"recall@{k}": statistics.fmean(r.recall[f"recall@{k}"] for r in results) for k in ks
    }
    metrics[f"mrr@{max_k}"] = statistics.fmean(r.reciprocal_rank for r in results)
    return EvalReport(
        retriever=retriever.name,
        split=split,
        created_at=datetime.now(UTC),
        n_questions=len(results),
        n_unanswerable_skipped=skipped,
        metrics={name: round(value, 4) for name, value in metrics.items()},
        mean_latency_ms=round(statistics.fmean(r.latency_ms for r in results), 2),
        results=results,
    )


def save_report(report: EvalReport, reports_dir: Path) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = report.created_at.strftime("%Y%m%d-%H%M%S")
    path = reports_dir / f"{stamp}-{report.retriever}-{report.split}.json"
    path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    return path
