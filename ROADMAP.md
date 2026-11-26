# Lộ trình 8 tuần

Khoảng 10 giờ mỗi tuần, từ 23/11/2026 đến 17/01/2027, thêm 1 tuần dự phòng trước Tết.
Đánh dấu `[x]` khi xong. Mỗi tuần có: các bước, bẫy cần biết, điều kiện "xong", gợi ý commit.

## Quy tắc chung

**Chia việc với AI**
- Phần lõi trong `src/quyche/` do bạn tự viết: `text.py`, `ingest/chunker.py`, `retrieval/bm25.py`, `evaluation/metrics.py`, cùng phần vector, RRF và prompt ở các tuần sau. AI chỉ được giải thích khái niệm, gợi ý hướng làm và review code bạn đã viết.
- AI được viết phần phụ: giao diện Gradio, Dockerfile, file cấu hình.
- Không commit dòng nào bạn chưa tự giải thích được. Thử giải thích thành tiếng như đang phỏng vấn.

**Thói quen hằng tuần**
- Commit nhỏ mỗi buổi làm, message rõ việc: `feat(chunker): bỏ tiêu đề chương khỏi cuối Điều`.
- Mỗi thí nghiệm là một mục trong [EXPERIMENTS.md](EXPERIMENTS.md), **kể cả khi thất bại**.
- Chủ nhật dành 15 phút ghi 3 dòng vào cuối EXPERIMENTS.md: tuần này làm gì, học được gì, vướng gì. Đây là nguyên liệu cho bài blog ở tuần 7.

**Cơ chế TODO**: test của phần lõi gắn marker `todo` và bị bỏ qua. Viết xong một hàm thì xóa dòng `pytestmark = pytest.mark.todo` (hoặc `@pytest.mark.todo`) trong file test tương ứng. Từ đó CI sẽ kiểm tra hàm đó.

```bash
uv run pytest -m todo      # xem các test còn phải làm
```

---

## Tuần 0 (23–29/11): Khởi động và dữ liệu

Mục tiêu: hiểu rõ bài toán, có văn bản và có câu hỏi thật. Chưa cần viết code lõi.

- [ ] Clone repo, chạy `uv sync` và `uv run pytest` (14 passed, 37 TODO). Kiểm tra tab Actions trên GitHub có xanh.
- [ ] **Tự viết** [docs/design.md](docs/design.md), không dùng AI. Đây là tài liệu bạn sẽ kể lại khi phỏng vấn.
- [ ] Gom văn bản vào `data/raw/`, ghi từng văn bản vào [docs/data-sources.md](docs/data-sources.md). Nguồn: website trường và phòng đào tạo, sổ tay sinh viên, văn bản của Bộ GD&ĐT.
  - Quy chế đào tạo đại học của trường, và Quy chế đào tạo trình độ đại học của Bộ GD&ĐT (Thông tư 08/2021/TT-BGDĐT; kiểm tra xem đã có văn bản sửa đổi chưa)
  - Quy định học phí, miễn giảm học phí
  - Quy định học bổng khuyến khích học tập
  - Quy định đánh giá kết quả rèn luyện
  - Quy chế công tác sinh viên
- [ ] Đặt tên file theo quy ước trong [data/README.md](data/README.md). Tên file chính là `doc_id`.
- [ ] Tạo Google Form "Bạn từng thắc mắc gì về quy chế của trường?". Chỉ hỏi câu hỏi, không thu tên hay mã sinh viên. Gửi vào nhóm lớp và câu lạc bộ.

**Bẫy cần biết**
- Nhiều file là **PDF scan** (ảnh chụp), không có lớp chữ. Ghi chú loại PDF ngay khi tải về.
- Văn bản mới có thể **thay thế** văn bản cũ. Ghi ngày hiệu lực và văn bản bị thay thế, tuần 6 sẽ cần.

**Xong khi:** có ít nhất 10 văn bản trong `data-sources.md` và ít nhất 30 phản hồi form.
**Gợi ý commit:** `docs: viết design.md`, `docs: thêm danh sách nguồn dữ liệu`.

---

## Tuần 1 (30/11–6/12): Đọc PDF và chia theo Điều

Mục tiêu: `uv run quyche ingest` biến mọi văn bản thành các Điều sạch sẽ.

- [ ] Chạy `uv run quyche inspect`, mở các file trong `data/processed/text/`, đọc text thô của từng văn bản. Liệt kê các ca khó **trước khi** viết chunker.
- [ ] Viết `normalize_text` và `tokenize` trong `src/quyche/text.py`, cho `tests/test_text.py` pass, xóa marker.
- [ ] Viết `split_into_articles` trong `src/quyche/ingest/chunker.py`, cho `tests/test_chunker.py` pass, xóa marker.
- [ ] Chạy `uv run quyche ingest` trên PDF thật. Mở `data/processed/chunks.jsonl` và đọc ngẫu nhiên 20 chunk.
- [ ] Mỗi lỗi gặp trong PDF thật: thêm một đoạn tái hiện vào `tests/fixtures/`, viết test, rồi mới sửa code.
- [ ] **Thí nghiệm E1:** chọn 20 trang khó, so pypdf (đang dùng), pymupdf và OCR (cho bản scan, ví dụ Tesseract với gói tiếng Việt). Chấm tay tỉ lệ đọc đúng. Chọn cách tốt nhất và cập nhật `ingest/pdf.py`.

**Bẫy cần biết**
- Dấu tiếng Việt dạng tổ hợp (NFD): hai chuỗi trông giống hệt nhau nhưng so sánh ra khác.
- Một file thường gồm **Quyết định ban hành** (Điều 1, 2, 3) và **Quy chế kèm theo** (lại Điều 1, 2...). Lệnh `ingest` sẽ cảnh báo chunk_id trùng. Bạn cần tự quyết cách xử lý (bỏ phần Quyết định, hoặc thêm tiền tố vào chunk_id) và ghi lý do vào EXPERIMENTS.md.
- Header và footer lặp lại ở mỗi trang (số trang, tên trường) chen vào giữa một Điều.
- pypdf thường làm **mất dòng trống**: đừng dựa vào dòng trống để tách Điều hay Chương.
- "Điều 5" xuất hiện giữa câu, hoặc đầu dòng do xuống dòng, không phải Điều mới.

**Cách test khi có file thật (ví dụ 3 văn bản)**

| Tầng | Khi nào | Làm gì |
|---|---|---|
| 0. Quan sát | Ngay khi có PDF | `uv run quyche inspect`: số trang, PDF chữ hay scan, số dòng giống tiêu đề Điều (ước lượng thô). Đọc text thô, ghi lại ca khó |
| 1. Unit test | Khi viết `text.py`, `chunker.py` | Mỗi ca khó: chép một đoạn ngắn vào `tests/fixtures/`, viết test nêu kết quả mong đợi, rồi mới sửa code. `uv run pytest tests/test_chunker.py -m todo` |
| 2. Tích hợp | Khi unit test đã pass | `uv run quyche ingest`. So "Số Điều" với Điều cuối cùng trong PDF và với số ước lượng của `inspect`; lệch thì tìm hiểu vì sao. Không được có cảnh báo trùng `chunk_id`. Đọc ngẫu nhiên 10 chunk, cùng Điều đầu, Điều cuối, chunk dài nhất và ngắn nhất |
| 3. Truy xuất | Tuần 2 | Mỗi văn bản khoảng 10 câu hỏi kèm đáp án vào `eval/questions.jsonl`, thử tay bằng `quyche search`, rồi `quyche eval` |

Số ước lượng của `inspect` thường **lớn hơn** số Điều thật, vì nó đếm cả tham chiếu bị xuống dòng ("Điều 3 của quy chế này") và cả phần Quyết định ban hành. Nó chỉ để đối chiếu, không phải đáp án.

**Xong khi:** mọi văn bản dạng chữ đã thành chunk có `doc_id`, số Điều, tiêu đề; test text và chunker đã bỏ marker; có kết luận E1.
**Gợi ý commit:** `feat(text): chuẩn hóa NFC`, `feat(chunker): tách Điều`, `fix(chunker): bỏ header trang`, `exp: E1 so sánh trích xuất PDF`.

---

## Tuần 2 (7–13/12): Bộ đánh giá và baseline BM25

Mục tiêu: có con số đầu tiên. Từ đây mọi thay đổi đều phải đo được.

- [ ] Làm sạch câu hỏi từ form vào `eval/questions.jsonl` theo [docs/eval-guidelines.md](docs/eval-guidelines.md). Gán đáp án đúng (văn bản + Điều) cho **ít nhất 100 câu**, trong đó khoảng 10% là câu không có đáp án.
- [ ] Chia ngẫu nhiên (cố định seed) thành dev 70 câu và test 30 câu. **Từ giờ không mở tập test** cho tới tuần 7.
- [ ] Xóa 3 câu ví dụ (`"example": true`).
- [ ] Viết `recall_at_k` và `reciprocal_rank`, cho `tests/test_metrics.py` pass, xóa marker.
- [ ] Viết `BM25Retriever`, cho `tests/test_bm25.py` pass, xóa marker. Xóa luôn marker của `test_eval_end_to_end` trong `tests/test_cli.py`.
- [ ] Kiểm tra chéo: so top-5 của bạn với thư viện `rank-bm25` trên 10 câu.
- [ ] `uv run quyche eval --retriever bm25`, ghi kết quả vào EXPERIMENTS.md và bảng kết quả trong README.
- [ ] **Thí nghiệm E2:** BM25 theo âm tiết so với theo từ đã tách (pyvi hoặc underthesea: "học phí" thành một token).
- [ ] Đọc báo cáo trong `eval/reports/`: 10 câu sai nhất sai vì sao? Ghi lại.

**Bẫy cần biết**
- Viết câu hỏi bằng cách chép câu trong quy chế sẽ làm BM25 trông tốt giả tạo. Giữ nguyên cách sinh viên gõ.
- Đừng chỉnh BM25 theo từng câu trong tập dev đến mức "học thuộc" tập dev.

**Xong khi:** `uv run quyche eval --retriever bm25` in ra Recall@5 và MRR thật; README có số đầu tiên.
**Gợi ý commit:** `data: 100 câu hỏi đánh giá`, `feat(metrics): recall và MRR`, `feat(bm25): baseline`, `exp: E2 tách từ`.

---

## Tuần 3 (14–20/12): Tìm kiếm vector và hybrid

Mục tiêu: biết khi nào BM25 thua, khi nào vector thua, và trộn chúng lại.

- [ ] Viết `retrieval/dense.py`: embed mọi chunk một lần, lưu ra file `.npy`, tìm bằng cosine với numpy. Đăng ký vào `REGISTRY` trong `retrieval/__init__.py`.
- [ ] **Thí nghiệm E3:** so 2–3 model embedding đa ngôn ngữ hoặc tiếng Việt, ví dụ `BAAI/bge-m3`, `intfloat/multilingual-e5-base` và một model embedding tiếng Việt trên Hugging Face. Ghi cả Recall và thời gian embed.
- [ ] Viết `retrieval/hybrid.py` với RRF tự cài đặt: `score(d) = Σ 1 / (k + rank_i(d))`, k = 60.
- [ ] **Thí nghiệm E4:** BM25, vector, hybrid. Có thể thêm trọng số cho từng nguồn.
- [ ] Chọn cấu hình tốt nhất trên dev, ghi lý do.

**Bẫy cần biết**
- Model e5 cần tiền tố `"query: "` và `"passage: "`. Quên tiền tố thì kết quả kém mà không báo lỗi.
- Điều quá dài vượt giới hạn token của model sẽ bị cắt mất phần sau.
- Corpus chỉ vài nghìn chunk: numpy là đủ, chưa cần vector DB. Hãy giải thích được lý do này.

**Xong khi:** EXPERIMENTS.md có ít nhất 4 cấu hình, đã chốt cấu hình dùng tiếp.
**Gợi ý commit:** `feat(dense): tìm kiếm vector`, `feat(hybrid): RRF`, `exp: E3 so sánh embedding`, `exp: E4 hybrid`.

---

## Tuần 4 (21–27/12): Sinh câu trả lời có trích dẫn

Tuần này dễ trùng ôn thi. Phần bắt buộc là 3 mục đầu, còn lại làm nếu kịp.

- [ ] Chọn LLM: API miễn phí, chạy local (Ollama) hay trả phí. So theo chi phí, độ trễ, chất lượng tiếng Việt. Ghi vào `docs/decisions/001-chon-llm.md` theo mẫu trong `docs/decisions/README.md`.
- [ ] Viết `generation/` với prompt chỉ trả lời dựa trên các Điều đã truy xuất, trích dẫn dạng `[doc_id, Điều X]`, và nói "Không tìm thấy trong quy chế" khi không đủ thông tin. Thêm lệnh `uv run quyche ask "..."`.
- [ ] Kiểm tra trích dẫn: mọi `[doc_id, Điều X]` trong câu trả lời phải nằm trong các chunk đã đưa cho model. Viết test.
- [ ] **Thí nghiệm E5:** chấm tay 30 câu trả lời trên dev theo 4 mức: đúng / thiếu / sai / bịa. Câu không có đáp án phải được trả lời "không tìm thấy".

**Bẫy cần biết**
- Không commit API key. Dùng biến môi trường và file `.env` (đã nằm trong `.gitignore`).
- Model hay "bịa" số tiền, số tín chỉ. Kiểm tra kỹ các con số trong câu trả lời.

**Xong khi:** `quyche ask` trả lời có trích dẫn; có tỉ lệ trả lời đúng trên 30 câu.
**Gợi ý commit:** `docs: ADR chọn LLM`, `feat(generation): trả lời có trích dẫn`, `feat(generation): kiểm tra trích dẫn`, `exp: E5 chấm tay`.

---

## Tuần 5 (28/12–3/1): Demo và người dùng thật

- [ ] Giao diện Gradio: ô hỏi, câu trả lời, các Điều được trích (bấm để xem nguyên văn), nút 👍/👎, ô góp ý.
- [ ] Ghi log mỗi lượt hỏi: thời gian, câu hỏi, các Điều truy xuất, câu trả lời, đánh giá. **Không ghi tên, email, mã sinh viên.** Ghi rõ trên giao diện rằng câu hỏi được lưu để cải thiện hệ thống.
- [ ] Deploy lên Hugging Face Spaces (miễn phí). Thêm link demo vào đầu README.
- [ ] Gửi cho ít nhất 30 bạn. Nhờ 3 bạn ngồi dùng thử trước mặt mình 10 phút, ghi lại chỗ họ lúng túng.

**Xong khi:** có link công khai và ít nhất 100 câu hỏi thật trong log.
**Gợi ý commit:** `feat(app): giao diện Gradio`, `feat(app): log và phản hồi`, `docs: link demo`.

---

## Tuần 6 (4–10/1): Học từ dữ liệu thật

- [ ] Đọc toàn bộ log, phân loại từng câu sai: (a) dữ liệu không có, (b) truy xuất sai, (c) dùng văn bản cũ đã hết hiệu lực, (d) LLM hiểu sai hoặc bịa.
- [ ] Vẽ bảng: mỗi nhóm bao nhiêu câu. Chọn **một** nhóm nhiều nhất để sửa. Ví dụ với nhóm (c): thêm metadata ngày hiệu lực và ưu tiên văn bản mới nhất.
- [ ] Thêm 20 câu sai lấy từ log vào tập dev (`"source": "log"`), đo lại trước và sau khi sửa (**E6**).
- [ ] Bổ sung văn bản còn thiếu nếu nhóm (a) lớn.

**Xong khi:** có một câu kiểu "từ X lên Y sau khi sửa Z", đo trên dev.
**Gợi ý commit:** `data: thêm câu hỏi từ log`, `feat: ưu tiên văn bản hiệu lực`, `exp: E6 sửa lỗi từ log thật`.

---

## Tuần 7 (11–17/1): Đóng gói và kể chuyện

- [ ] Chạy tập test **đúng một lần**: `uv run quyche eval --split test --confirm-test`. Ghi kết quả, không chỉnh gì thêm theo tập test.
- [ ] README: link demo, bảng kết quả, sơ đồ kiến trúc, hạn chế, hướng phát triển, số người dùng.
- [ ] Quay video demo 2 phút (hỏi 3 câu: một câu dễ, một câu khó, một câu không có đáp án).
- [ ] Viết blog trên Viblo: bài toán, cách đo, 3 thí nghiệm thú vị nhất, sai lầm lớn nhất. Dùng phần ghi chép chủ nhật.
- [ ] Cập nhật CV và profile README, ghim repo này lên đầu.
- [ ] Ôn bộ câu hỏi phỏng vấn cho chính dự án này.

**Xong khi:** CV có gạch đầu dòng với số liệu thật của bạn.
**Gợi ý commit:** `docs: kết quả cuối trên tập test`, `docs: README hoàn chỉnh`.

---

## Tuần 8 (18–24/1): Dự phòng

Dành cho tuần thi hoặc tuần bị trễ. Nếu đã xong hết, chọn một mục nâng cao:
- [ ] Reranker (cross-encoder) sau bước hybrid, đo lại.
- [ ] Chia chunk tới mức Khoản, so với mức Điều.
- [ ] Đánh giá tự động câu trả lời bằng LLM làm giám khảo, so với điểm chấm tay ở E5.
