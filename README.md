# YOLOv8_app
Đây là một trang web đơn giản được xây dựng bằng Flask và YOLOv8n (nano) để phát hiện đối tượng trong ảnh. Việc chọn YOLOv8n (nano) thay vì YOLOv8m, YOLOv8s, YOLOv8l, hoặc YOLOv8x thường dựa trên cân bằng giữa tốc độ, độ chính xác và tài nguyên hệ thống. Tại đây người dùng có thể upload ảnh, nhận kết quả ảnh được detect, các ảnh đã upload sẽ được lưu trữ cùng với kết quả detect và có thể tìm kiếm ảnh dựa trên tên nhãn.

## Cách sử dụng

1. Tạo môi trường ảo
```
python -m venv venv
```
2. Cài đặt các package cần thiết
```
pip install -r requirements.txt
```
3. Chạy file app.py 
```
py app.py
```
4. Truy cập vào trang web http://localhost:5000

5. Chọn ảnh để phát hiện

6. Chọn trang "Ảnh đã upload" để xem các ảnh đã upload

7. Nhập tên nhãn để tìm kiếm


## Cấu trúc thư mục
```
yolo_v8_app/
│── app.py                  # Tập tin chính để chạy Flask web server
│── requirement.txt         # Danh sách các thư viện cần cài đặt
│── yolov8n.pt              # Mô hình YOLOv8 để detect đối tượng
├── static/                 # Thư mục chứa các file tĩnh như ảnh, CSS, kết quả
│   ├── results/            # Ảnh đã detect xong (ảnh đầu ra với bounding boxes)
│   ├── Images/             # Ảnh cho trang web
│   ├── results_json/       # Lưu các kết quả detect ở dạng file .json
│   ├── uploads/            # Ảnh người dùng upload lên để xử lý
│   └── styles.css          # css giao diện web
│── templates/
│    └── index.html         # Trang chủ - nơi upload ảnh
│   ├── result.html         # Trang hiển thị kết quả sau khi detect
│   ├── search.html         # Trang tìm kiếm ảnh theo nhãn đã detect
│   └── uploads.html        # Trang liệt kê tất cả ảnh đã upload + xóa ảnh
```
