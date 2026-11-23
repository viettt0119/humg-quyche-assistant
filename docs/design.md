# Tài liệu thiết kế

> **Tự viết toàn bộ file này, không dùng AI.** Viết ngắn, bằng lời của bạn. Đây là thứ bạn sẽ kể lại khi phỏng vấn, và là thước đo để quyết định làm gì, bỏ gì trong 8 tuần tới. Xóa các dòng hướng dẫn in nghiêng khi viết xong.

## 1. Bài toán

_Sinh viên đang gặp khó khăn gì khi tìm hiểu quy chế? Hiện họ giải quyết bằng cách nào (hỏi nhóm lớp, hỏi cố vấn học tập, tự đọc PDF)? Cách đó dở ở đâu? Một ví dụ có thật mà bạn hoặc bạn bè đã gặp._

## 2. Người dùng

_Ai sẽ dùng? Sinh viên năm mấy, ngành nào? Họ hỏi lúc nào (đầu kỳ đăng ký học, lúc bị cảnh báo, lúc làm hồ sơ tốt nghiệp)? Họ dùng điện thoại hay máy tính?_

## 3. Mười câu hỏi tiêu biểu

_Viết đúng giọng sinh viên sẽ gõ, kể cả viết tắt và không dấu nếu có._

1.
2.
3.
4.
5.
6.
7.
8.
9.
10.

## 4. Thế nào là thành công

_Chọn con số cụ thể và lý do chọn._
- Truy xuất: Recall@5 trên tập dev ≥ ___
- Câu trả lời: tỉ lệ đúng khi chấm tay ≥ ___ ; tỉ lệ bịa ≤ ___
- Người dùng: ít nhất ___ người dùng thật, ___ câu hỏi; tỉ lệ 👍 ≥ ___
- Độ trễ: trả lời trong ___ giây

## 5. Phạm vi

**Làm:**
-

**Không làm (và vì sao):**
- _Ví dụ: không tra cứu điểm hay lịch học cá nhân, vì cần đăng nhập hệ thống của trường._
-

## 6. Rủi ro và cách xử lý

| Rủi ro | Khả năng | Cách xử lý |
|---|---|---|
| _Văn bản là PDF scan, OCR sai nhiều_ | | |
| _Trả lời sai làm sinh viên thiệt thòi_ | | _Luôn kèm trích dẫn và lời nhắc kiểm tra với phòng đào tạo_ |
| _Không đủ người dùng thử_ | | |
|  | | |

## 7. Kiến trúc dự kiến

_Vẽ bằng chữ hoặc mermaid: PDF → trích text → chia Điều → chỉ mục (BM25, vector) → truy xuất → LLM → câu trả lời có trích dẫn. Cập nhật khi thay đổi._

## 8. Thay đổi so với kế hoạch ban đầu

_Ghi lại mỗi lần bạn đổi hướng và lý do. Phần này rất đáng giá khi phỏng vấn._
