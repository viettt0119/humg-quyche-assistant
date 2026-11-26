# Trợ lý quy chế HUMG

[![CI](https://github.com/viettt0119/humg-quyche-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/viettt0119/humg-quyche-assistant/actions/workflows/ci.yml)

Sinh viên hỏi về quy chế (cảnh báo học tập, học phí, học bổng, điều kiện tốt nghiệp...) bằng lời của mình. Trợ lý trả lời và **trích dẫn đúng văn bản, Điều, Khoản** để sinh viên tự kiểm tra lại.

> **Trạng thái:** Tuần 0/8. Đang thu thập văn bản và câu hỏi. Lộ trình chi tiết: [ROADMAP.md](ROADMAP.md)

## Vì sao làm dự án này

Quy chế nằm rải rác trong nhiều file PDF dài, có văn bản sửa đổi chồng lên văn bản cũ. Sinh viên thường hỏi nhau trong nhóm lớp và nhận câu trả lời không chắc chắn. Mục tiêu: trả lời nhanh, **có nguồn**, và biết nói "không tìm thấy" khi dữ liệu không có.

Chi tiết bài toán, người dùng và tiêu chí thành công: [docs/design.md](docs/design.md)

## Kết quả

Đo trên tập dev do tự xây từ câu hỏi thật của sinh viên ([cách xây](docs/eval-guidelines.md)). Nhật ký đầy đủ: [EXPERIMENTS.md](EXPERIMENTS.md)

| Cấu hình | Recall@5 | MRR@10 | Ghi chú |
|---|---|---|---|
| _Chưa có. Số đầu tiên dự kiến ở tuần 2 (baseline BM25)._ | | | |

## Chạy thử

Yêu cầu: Python ≥ 3.12 và [uv](https://docs.astral.sh/uv/getting-started/installation/). Chạy các lệnh từ thư mục gốc của repo.

```bash
uv sync
```

```bash
uv run quyche inspect                       # xem text thô từng PDF, PDF chữ hay scan
```

```bash
uv run quyche ingest                        # đọc PDF trong data/raw/, chia theo Điều
```

```bash
uv run quyche search "điều kiện tốt nghiệp"  # tìm các Điều liên quan
```

```bash
uv run quyche eval --retriever bm25         # đo Recall@k và MRR trên tập dev
```

Kiểm tra code:

```bash
uv run ruff check . && uv run ruff format --check . && uv run pytest
```

## Cấu trúc

```
src/quyche/
  text.py               chuẩn hóa và tách token tiếng Việt
  ingest/pdf.py         trích text từ PDF
  ingest/chunker.py     chia văn bản theo Điều
  retrieval/bm25.py     BM25 tự cài đặt
  evaluation/metrics.py Recall@k, MRR
  evaluation/runner.py  chạy bộ đánh giá, xuất báo cáo
  cli.py                lệnh quyche
data/                   văn bản gốc (PDF để ngoài git) và chunk đã xử lý
eval/questions.jsonl    bộ câu hỏi đánh giá
docs/                   thiết kế, nguồn dữ liệu, hướng dẫn gán nhãn, quyết định kỹ thuật
```

## Dự án được làm như thế nào

Khung ban đầu (công cụ, cấu trúc thư mục, CLI, khung đánh giá) được dựng cùng Claude Code. Phần lõi gồm chuẩn hóa văn bản, chia Điều, BM25, metric, tìm kiếm vector, trộn kết quả và prompt do mình tự viết, có test đi kèm. Mọi thí nghiệm, kể cả thất bại, được ghi trong [EXPERIMENTS.md](EXPERIMENTS.md).

## Giấy phép

Mã nguồn: [MIT](LICENSE). Văn bản quy chế thuộc về cơ quan ban hành; repo chỉ ghi nguồn và đường dẫn, không phân phối lại file PDF.
