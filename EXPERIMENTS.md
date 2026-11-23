# Nhật ký thí nghiệm

Mỗi thí nghiệm một mục, **kể cả khi thất bại**. Một thí nghiệm thất bại được ghi lại cẩn thận có giá trị ngang một thí nghiệm thành công: nó cho thấy bạn biết đặt giả thuyết và đọc kết quả.

Quy tắc:
- Mỗi lần chỉ đổi **một** thứ so với cấu hình đang tốt nhất.
- Luôn đo trên **dev**. Tập test chỉ chạy một lần ở tuần 7.
- Dán đường dẫn file báo cáo trong `eval/reports/` nếu có (nhớ copy ra ngoài nếu muốn giữ, vì thư mục đó không nằm trong git).

## Bảng tổng hợp

| # | Ngày | Thay đổi | Recall@5 | MRR@10 | Kết luận |
|---|---|---|---|---|---|
| | | | | | |

## Mẫu cho một thí nghiệm

```markdown
### E? — <tên ngắn>
- **Ngày:**
- **Giả thuyết:** Tôi nghĩ <thay đổi> sẽ <tăng/giảm metric> vì <lý do>.
- **Thay đổi:** <so với cấu hình nào, đổi đúng một thứ gì>
- **Kết quả:** <bảng số trước/sau>
- **Ví dụ cụ thể:** <1–2 câu hỏi mà kết quả thay đổi, và vì sao>
- **Kết luận:** <giữ hay bỏ, bước tiếp theo>
```

## Các thí nghiệm dự kiến

### E1 — So sánh cách trích text từ PDF (tuần 1)
_Chưa làm._ pypdf vs pymupdf vs OCR trên 20 trang khó, chấm tay tỉ lệ đọc đúng.

### E2 — BM25 theo âm tiết vs theo từ (tuần 2)
_Chưa làm._

### E3 — So sánh model embedding (tuần 3)
_Chưa làm._

### E4 — BM25 vs vector vs hybrid RRF (tuần 3)
_Chưa làm._

### E5 — Chấm tay 30 câu trả lời (tuần 4)
_Chưa làm._ Đúng / thiếu / sai / bịa.

### E6 — Sửa nhóm lỗi lớn nhất từ log thật (tuần 6)
_Chưa làm._

## Ghi chép hằng tuần

<!-- Chủ nhật: 3 dòng. Làm được gì? Học được gì? Vướng gì? -->
