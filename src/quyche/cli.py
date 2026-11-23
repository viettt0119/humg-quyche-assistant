"""Dòng lệnh: quyche ingest | search | eval.

File này là hạ tầng, viết sẵn. Khi một hàm lõi chưa được cài đặt, lệnh in ra hướng dẫn
thay vì traceback.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterator
from contextlib import contextmanager
from enum import StrEnum
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from quyche.config import get_settings
from quyche.evaluation.runner import evaluate, load_questions, save_report
from quyche.ingest.chunker import split_into_articles
from quyche.ingest.pdf import load_document, looks_scanned
from quyche.jsonl import read_jsonl, write_jsonl
from quyche.retrieval import REGISTRY, build_retriever
from quyche.schemas import Chunk
from quyche.text import normalize_text

app = typer.Typer(help="Trợ lý quy chế HUMG.", no_args_is_help=True, add_completion=False)
console = Console()


class Split(StrEnum):
    dev = "dev"
    test = "test"


@contextmanager
def guided() -> Iterator[None]:
    """Đổi lỗi thường gặp thành thông báo dễ hiểu và exit code 1."""
    try:
        yield
    except NotImplementedError as e:
        console.print(f"[yellow]Chưa cài đặt:[/] {e}")
        raise typer.Exit(1) from None
    except ValueError as e:
        console.print(f"[red]Lỗi:[/] {e}")
        raise typer.Exit(1) from None


def _require(path: Path, hint: str) -> None:
    if not path.exists():
        console.print(f"[red]Chưa có[/] {path}. {hint}")
        raise typer.Exit(1)


def _load_chunks(path: Path) -> list[Chunk]:
    _require(path, "Bỏ PDF vào data/raw/ rồi chạy: uv run quyche ingest")
    return read_jsonl(path, Chunk)


@app.command()
def ingest() -> None:
    """Đọc mọi PDF trong data/raw/, chia theo Điều, ghi ra data/processed/chunks.jsonl."""
    settings = get_settings()
    pdfs = sorted(settings.raw_dir.glob("*.pdf"))
    if not pdfs:
        console.print(
            f"[red]Chưa có PDF nào trong[/] {settings.raw_dir}/. Xem docs/data-sources.md."
        )
        raise typer.Exit(1)

    table = Table("doc_id", "Trang", "Số Điều", "Ghi chú")
    chunks: list[Chunk] = []
    with guided():
        for pdf in pdfs:
            doc = load_document(pdf)
            if looks_scanned(doc):
                table.add_row(doc.doc_id, str(len(doc.pages)), "0", "[yellow]PDF scan? Cần OCR[/]")
                continue
            doc_chunks = split_into_articles(normalize_text("\n".join(doc.pages)), doc.doc_id)
            note = "" if doc_chunks else "[yellow]Không tìm thấy Điều nào[/]"
            table.add_row(doc.doc_id, str(len(doc.pages)), str(len(doc_chunks)), note)
            chunks.extend(doc_chunks)

    console.print(table)
    duplicates = [cid for cid, n in Counter(c.chunk_id for c in chunks).items() if n > 1]
    if duplicates:
        console.print(
            f"[yellow]Cảnh báo:[/] {len(duplicates)} chunk_id bị trùng, ví dụ {duplicates[0]}. "
            "Văn bản có thể gồm Quyết định ban hành và Quy chế kèm theo, mỗi phần đều có "
            "Điều 1, Điều 2... Xem ROADMAP tuần 1."
        )
    count = write_jsonl(settings.chunks_path, chunks)
    console.print(f"Đã ghi {count} chunk vào {settings.chunks_path}")


@app.command()
def search(
    query: str = typer.Argument(..., help="Câu hỏi"),
    retriever: str = typer.Option("bm25", "--retriever", "-r", help="Tên bộ truy xuất"),
    k: int = typer.Option(5, "-k", help="Số kết quả"),
) -> None:
    """Tìm các Điều liên quan tới câu hỏi."""
    chunks = _load_chunks(get_settings().chunks_path)
    with guided():
        hits = build_retriever(retriever, chunks).search(query, k=k)
    if not hits:
        console.print("Không tìm thấy kết quả nào.")
        return
    for hit in hits:
        c = hit.chunk
        snippet = " ".join(c.text.split())[:160]
        console.print(
            f"[bold]{hit.rank}.[/] [cyan]{c.doc_id}[/] Điều {c.article}. {c.article_title}"
            f"  [dim](điểm {hit.score:.3f})[/]\n   {snippet}…"
        )


@app.command("eval")
def eval_cmd(
    retriever: str = typer.Option("bm25", "--retriever", "-r", help="Tên bộ truy xuất"),
    split: Split = typer.Option(Split.dev, "--split", help="dev: dùng hằng ngày; test: chỉ 1 lần"),
    confirm_test: bool = typer.Option(False, "--confirm-test", help="Xác nhận chạy tập test"),
    save: bool = typer.Option(True, "--save/--no-save", help="Lưu báo cáo JSON vào eval/reports/"),
) -> None:
    """Đo Recall@k và MRR của một bộ truy xuất trên bộ câu hỏi đánh giá."""
    if split is Split.test and not confirm_test:
        console.print(
            "[yellow]Tập test chỉ chạy MỘT lần ở tuần 7[/], sau khi đã chốt cấu hình trên dev. "
            "Nếu đúng là lúc đó, thêm --confirm-test."
        )
        raise typer.Exit(1)

    settings = get_settings()
    chunks = _load_chunks(settings.chunks_path)
    _require(settings.questions_path, "Xem docs/eval-guidelines.md.")
    questions = load_questions(settings.questions_path, split.value)
    if not questions:
        console.print(
            f"Chưa có câu hỏi thật nào cho split '{split.value}' (câu ví dụ bị bỏ qua). "
            "Xem docs/eval-guidelines.md."
        )
        raise typer.Exit(1)

    with guided():
        report = evaluate(build_retriever(retriever, chunks), questions, split=split.value)

    table = Table(f"{retriever} · {split.value} · {report.n_questions} câu", "Giá trị")
    for name, value in report.metrics.items():
        table.add_row(name, f"{value:.3f}")
    table.add_row("độ trễ TB (ms)", f"{report.mean_latency_ms:.1f}")
    console.print(table)
    if report.n_unanswerable_skipped:
        console.print(f"Bỏ qua {report.n_unanswerable_skipped} câu không có đáp án trong dữ liệu.")
    if save:
        console.print(f"Báo cáo: {save_report(report, settings.reports_dir)}")


@app.command("retrievers")
def list_retrievers() -> None:
    """Liệt kê các bộ truy xuất đã đăng ký."""
    for name in sorted(REGISTRY):
        console.print(name)


if __name__ == "__main__":
    app()
