# Dữ liệu

```
data/
  raw/          PDF gốc, KHÔNG đưa lên git. Nguồn ghi trong docs/data-sources.md
  processed/
    chunks.jsonl   sinh bởi `uv run quyche ingest`, mỗi dòng một Điều
```

## Quy ước tên file PDF

Tên file (bỏ đuôi `.pdf`) chính là `doc_id`, xuất hiện trong mọi trích dẫn. Đặt tên:
- chữ thường, không dấu, nối bằng gạch ngang
- dạng `<loai-van-ban>-<chu-de>-<nam>`

Ví dụ: `quy-che-dao-tao-2021.pdf`, `quy-dinh-hoc-phi-2025.pdf`, `tt-08-2021-quy-che-dao-tao-dai-hoc.pdf`.

**Không đổi tên file sau khi đã gán nhãn câu hỏi**, vì `gold` trong `eval/questions.jsonl` tham chiếu tới `doc_id`.

## Schema của `chunks.jsonl`

| Trường | Ví dụ | Ý nghĩa |
|---|---|---|
| `chunk_id` | `quy-che-dao-tao-2021:dieu-12` | Mã duy nhất |
| `doc_id` | `quy-che-dao-tao-2021` | Văn bản chứa Điều này |
| `article` | `12` | Số Điều |
| `article_title` | `Cảnh báo kết quả học tập` | Tiêu đề Điều |
| `clause` | `null` | Số Khoản, nếu sau này chia tới Khoản |
| `text` | `Điều 12. Cảnh báo ...` | Toàn văn Điều |
