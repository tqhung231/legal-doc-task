# Bài test: Pipeline tiếp nhận văn bản pháp luật + Giao diện kiểm tra (QA Console)

## Bối cảnh

Sản phẩm của chúng tôi làm việc với văn bản pháp luật Việt Nam và sử dụng chúng cho
tìm kiếm / RAG. Trước khi văn bản đi vào pipeline RAG, cần một **hệ thống staging** để
tiếp nhận văn bản mới hoặc văn bản có thay đổi, chuẩn hóa, trích xuất metadata, phát hiện
trùng lặp / cập nhật, và cho phép người rà soát kiểm tra kết quả.

Repo này đã cung cấp sẵn mọi thứ để bạn bắt đầu: một bộ dữ liệu **mô phỏng (synthetic)**
gồm các văn bản pháp luật (`data/`) và một khung dự án tối giản. Bạn xây dựng pipeline và
giao diện kiểm tra trên nền tảng đó.

> Bạn **không** cần xây crawler, embedding thật, hay một hệ thống RAG hoàn chỉnh. Bài test
> tập trung vào mô hình hóa dữ liệu sạch sẽ, pipeline tiếp nhận có thể chạy lại, khả năng
> hiểu văn bản pháp luật, và tính dễ kiểm tra (inspectability).

## Mục tiêu

Xây dựng một ứng dụng nhỏ:

1. Tiếp nhận danh sách văn bản trong `data/feed.json`.
2. Lưu vào cơ sở dữ liệu.
3. Phân tích cấu trúc pháp lý (`Chương` / `Mục` / `Điều` / `Khoản` / `Điểm`).
4. Phát hiện văn bản trùng lặp và phiên bản cập nhật.
5. Cung cấp giao diện đơn giản để kiểm tra metadata và chất lượng văn bản đã trích xuất.

## Yêu cầu

### 1. Tiếp nhận (Ingestion)

Viết một lệnh (hoặc API) đọc `data/feed.json`, nạp từng tệp văn bản thô trong `data/raw/`
và lưu kết quả vào cơ sở dữ liệu. Điểm khởi đầu có sẵn tại [`ingest.py`](ingest.py):

```bash
python ingest.py data/feed.json
```

Với mỗi văn bản, lưu tối thiểu: văn bản thô, văn bản đã chuẩn hóa, source URL, mã băm nội
dung (content hash), và **trạng thái tiếp nhận**: `new`, `duplicate`, `updated`, hoặc `failed`.

Quá trình tiếp nhận phải **idempotent**: chạy lại cùng dữ liệu đầu vào không được tạo ra
văn bản trùng. Gợi ý logic:

```
cùng document_number + cùng content_hash        -> duplicate (trùng lặp)
cùng document_number + khác content_hash         -> updated (phiên bản cập nhật)
document_number mới                               -> new (văn bản mới)
```

### 2. Trích xuất metadata

Trích xuất tối thiểu: `title`, `document_number`, `document_type`, `issuing_authority`,
`issue_date`, `effective_date`, và `status` nếu có. Nếu không trích xuất được một trường,
lưu `null` và ghi lại một **cảnh báo** thay vì lỗi âm thầm.

### 3. Phân tích cấu trúc pháp lý

Phân tích văn bản thành cấu trúc pháp lý và lưu dưới dạng JSON.

- **Tối thiểu:** `Điều`, `Khoản`
- **Nâng cao (bonus):** `Chương`, `Mục`, `Điểm`

Điều này quan trọng với RAG pháp lý: chia theo cửa sổ token cố định thường kém; văn bản
pháp luật nên được chia theo đơn vị có ý nghĩa (điều, khoản, điểm).

### 4. Vấn đề chất lượng (QA)

Ghi cảnh báo cho các vấn đề như: thiếu số hiệu văn bản, thiếu ngày hiệu lực, văn bản trùng,
phân tích cấu trúc thất bại, hoặc phát hiện văn bản có dấu hiệu sửa đổi / thay thế nhưng
chưa liên kết được.

### 5. Giao diện (UI)

Xây dựng giao diện kiểm tra đơn giản gồm:

- **Danh sách lần tiếp nhận** (thời gian, tổng số, số lượng new/updated/duplicate/failed, cảnh báo),
- **Danh sách văn bản** (tiêu đề, số hiệu, loại, cơ quan, ngày ban hành/hiệu lực, trạng thái,
  trạng thái tiếp nhận) kèm bộ lọc cơ bản,
- **Trang chi tiết văn bản** hiển thị metadata, văn bản thô so với văn bản đã chuẩn hóa, cây
  cấu trúc pháp lý, cảnh báo, văn bản liên quan, và — nếu có làm — bản xem trước chunk cho RAG.

Mục đích của UI là **khả năng kiểm tra**, không phải vẻ đẹp: người rà soát có nhanh chóng
nhận ra pipeline trích xuất văn bản đúng hay không?

### 6. README

Trong bài nộp, giải thích cách cài đặt phụ thuộc, chạy migration (nếu có), chạy ingestion,
khởi động UI, và lý do đằng sau thiết kế schema cũng như các lựa chọn của bạn.

## Lưu ý về dữ liệu

Bộ dữ liệu trong `data/` cố tình có nhiều tình huống khó. Nó bao gồm, trong số đó: một văn
bản luật sạch và có cấu trúc rõ ràng, văn bản trùng lặp, một luật sửa đổi luật trước đó, một
văn bản được ban hành lại, một văn bản thiếu trường thông tin, và một tệp định dạng lộn xộn.
Pipeline của bạn phải xử lý tất cả một cách an toàn — **một văn bản lỗi không được làm hỏng
cả lần chạy.** Xem [`data/README.md`](data/README.md) để biết định dạng feed.

## Phần nâng cao (Bonus)

- Trích xuất văn bản liên quan từ các cụm như `sửa đổi, bổ sung`, `thay thế`, `hướng dẫn`.
- Sinh chunk sẵn sàng cho RAG theo đơn vị pháp lý (điều/khoản), kèm metadata.
- Thêm tìm kiếm theo tiêu đề, số hiệu văn bản và nội dung điều.
- Thêm test cơ bản cho trích xuất metadata và phát hiện trùng lặp (thư mục `tests/` đã được tạo sẵn).

## Gợi ý công nghệ (không bắt buộc)

Repo được thiết lập sẵn dưới dạng dự án Python, nên lựa chọn tự nhiên là **Python + SQLite +
một UI đơn giản** (ví dụ Streamlit hoặc Flask). Bạn được tự do dùng ngôn ngữ, cơ sở dữ liệu
hoặc framework khác — nếu vậy, hãy giữ `data/` làm đầu vào và giải thích cách chạy trong
README của bạn. Gợi ý phụ thuộc được liệt kê (dạng comment) trong [`pyproject.toml`](pyproject.toml).

## Bắt đầu

```bash
# 1. (gợi ý) tạo môi trường và cài đặt phụ thuộc bạn chọn
uv sync                 # hoặc: python -m venv .venv && pip install ...

# 2. chạy điểm khởi đầu ingestion với feed
python ingest.py data/feed.json

# 3. xây dựng pipeline, cơ sở dữ liệu và UI từ đây
```

## Tiêu chí đánh giá

Chúng tôi coi trọng **mô hình hóa dữ liệu sạch sẽ, pipeline tiếp nhận chạy lại được, và khả
năng hiểu văn bản pháp luật** hơn là độ trau chuốt của UI. Hãy thể hiện tư duy của bạn qua
schema, cách xử lý dữ liệu lộn xộn / thiếu, và README. Phạm vi bài làm khoảng **1–2 ngày**.
