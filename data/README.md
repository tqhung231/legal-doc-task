# Dữ liệu mẫu

Các tệp này là một bộ dữ liệu **mô phỏng, được tạo giả lập (synthetic)** phục vụ cho bài
test này. Các văn bản **không phải là văn bản pháp luật Việt Nam có thật** — nội dung, số
hiệu văn bản, ngày tháng và người ký đều là hư cấu. Chúng mô phỏng định dạng và cấu trúc của
văn bản pháp luật thật (khối tiêu đề, phần `Căn cứ…`, `Chương` / `Mục` / `Điều` / `Khoản` /
`Điểm`, khối chữ ký) để bạn có thể xây dựng và kiểm thử một pipeline tiếp nhận thực tế mà
không cần crawl bất kỳ nguồn trực tuyến nào.

## Cấu trúc thư mục

```
data/
  feed.json        # feed tiếp nhận — bắt đầu từ đây
  raw/             # các tệp văn bản thô được feed tham chiếu tới
```

## feed.json

Một mảng JSON. Mỗi phần tử mô tả một văn bản cần tiếp nhận:

| Trường          | Ý nghĩa                                                                |
|-----------------|------------------------------------------------------------------------|
| `source_url`    | Nơi văn bản được cho là lấy về (hư cấu).                               |
| `raw_file`      | Tệp trong `raw/` chứa văn bản thô.                                     |
| `expected_type` | Một **gợi ý sơ bộ** về loại văn bản lấy từ danh sách nguồn.            |

`expected_type` chỉ là gợi ý. Nó có thể là `null`, và không bảo đảm đúng — pipeline của bạn
vẫn phải tự xác định loại văn bản thật từ nội dung văn bản, và ghi một cảnh báo nếu hai giá
trị này không khớp.

## Bộ dữ liệu có gì

Bộ dữ liệu cố tình bao gồm các trường hợp lộn xộn và khó — văn bản trùng lặp, một luật sửa
đổi, một văn bản được ban hành lại, một văn bản thiếu trường thông tin, và một tệp định dạng
xấu. Một phần của bài test là xử lý chúng một cách an toàn (xem `README.md` ở thư mục gốc).
Việc xác định *tệp nào* ứng với *trường hợp nào* cũng là một phần của bài tập.
