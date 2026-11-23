# Hướng dẫn xây bộ câu hỏi đánh giá

Bộ câu hỏi là thước đo của cả dự án. Thước đo sai thì mọi con số sau đó đều vô nghĩa, nên phần này đáng làm chậm và cẩn thận.

## Định dạng

Mỗi dòng trong `eval/questions.jsonl` là một câu hỏi:

```json
{"qid": "q001", "question": "học lại 1 môn thì đóng tiền thế nào ạ", "gold": [{"doc_id": "quy-dinh-hoc-phi-2025", "article": "7"}], "split": "dev", "source": "form", "notes": ""}
```

| Trường | Ý nghĩa |
|---|---|
| `qid` | Mã duy nhất, không đổi về sau (`q001`, `q002`...) |
| `question` | Câu hỏi, giữ nguyên cách sinh viên viết |
| `gold` | Danh sách **mọi** Điều cần có để trả lời đủ. Để `[]` nếu dữ liệu không có đáp án |
| `split` | `dev` (dùng hằng ngày) hoặc `test` (khóa tới tuần 7) |
| `source` | `form` (từ Google Form), `log` (từ người dùng thật ở tuần 6), `self` (bạn tự viết) |
| `notes` | Ghi chú khi gán nhãn còn phân vân |

`article` là số Điều dạng chuỗi, đúng như chunker tạo ra (`"12"`, `"12a"`). Kiểm tra bằng cách tìm trong `data/processed/chunks.jsonl`.

## Quy tắc viết câu hỏi

1. **Giữ nguyên lời sinh viên**, kể cả viết tắt, không dấu, sai chính tả nhẹ. Đó là dữ liệu thật hệ thống sẽ gặp.
2. **Không chép câu chữ từ quy chế** để đặt câu hỏi. Câu hỏi trùng từ với văn bản sẽ làm BM25 trông tốt giả tạo.
3. Mỗi câu hỏi **một ý**. Câu hỏi hai ý thì tách thành hai câu.
4. Khoảng **10% câu không có đáp án** trong dữ liệu (`gold: []`), để kiểm tra hệ thống biết nói "không tìm thấy". Các câu này bị bỏ qua khi tính Recall nhưng dùng cho tuần 4.
5. Hạn chế câu `self`. Ưu tiên câu thật từ form và log.

## Quy tắc gán đáp án

1. Đọc Điều đó trong văn bản gốc, không gán theo trí nhớ.
2. Cần hai Điều mới trả lời đủ thì ghi cả hai.
3. Hai văn bản cùng quy định một việc (ví dụ quy chế của Bộ và quy chế của trường): ghi văn bản đang được áp dụng; nếu cả hai đều đúng thì ghi cả hai và giải thích ở `notes`.
4. Phân vân thì ghi vào `notes` và nhờ một người khác xem lại. Nếu được, nhờ một bạn khác gán độc lập 20 câu rồi so: tỉ lệ đồng ý thấp nghĩa là hướng dẫn chưa rõ.

## Chia dev và test

- Trộn ngẫu nhiên với seed cố định, 70% dev và 30% test. Cố gắng để mỗi chủ đề (học phí, học vụ, tốt nghiệp...) đều có mặt ở cả hai.
- **Tập test bị khóa**: không đọc, không chạy, không sửa cho tới tuần 7. CLI bắt buộc thêm `--confirm-test` để nhắc điều này.
- Câu thêm sau này (từ log ở tuần 6) đi vào dev.
