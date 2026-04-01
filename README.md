# 🏃‍♂️ Smart Fall Detection System

Hệ thống phát hiện té ngã thông minh sử dụng kết hợp Computer Vision và Deep Learning, được tối ưu để chạy theo thời gian thực (Real-time).

## Tính năng nổi bật
* **Giảm thiểu báo động giả (False Positives):** Kết hợp thuật toán tính toán vận tốc trục Y (hiện tượng rơi tự do) và phân tích tư thế (vai thấp hơn hông) để phân biệt giữa việc "bị ngã đột ngột" và "chủ động nằm/ngồi".
* **Theo dõi đa mục tiêu (Multi-object Tracking):** Sử dụng YOLOv8 để phát hiện, gán ID và theo dõi trạng thái độc lập của từng người trong khung hình.
* **Phân tích tư thế chính xác:** Tích hợp MediaPipe Pose để trích xuất các điểm neo (landmarks) trên cơ thể con người.
* **Cảnh báo đa luồng (Multi-threading):** Hệ thống âm thanh cảnh báo (Alarm) được thiết lập chạy trên một luồng (thread) hoàn toàn riêng biệt, đảm bảo không gây giật lag hay giảm FPS cho luồng xử lý camera chính.

## Cấu trúc dự án
```text
├── Code/
│   ├── alert_system.py      # Module quản lý luồng âm thanh cảnh báo
│   ├── fall_detector.py     # Module chứa logic xử lý AI (YOLO, MediaPipe)
│   ├── main.py              # File chạy chính, điều phối hệ thống
│   └── requirements.txt     # Danh sách các thư viện cần cài đặt
├── README.md                # Tài liệu giới thiệu và hướng dẫn (Bạn đang đọc nó)
```

##  Hướng dẫn cài đặt và sử dụng

### 1. Yêu cầu hệ thống
* Python 3.8 trở lên.
* Hệ điều hành: **Windows** (Do module âm thanh hiện tại đang sử dụng thư viện `winsound` đặc thù của Windows). *Nếu bạn sử dụng MacOS/Linux, cần tinh chỉnh lại file `alert_system.py` bằng các thư viện đa nền tảng như `pygame` hoặc `playsound`.*
* Webcam máy tính hoặc Camera gắn ngoài.

### 2. Cài đặt môi trường
Clone repository này về máy, mở terminal/command prompt tại thư mục `Code/` và chạy lệnh sau để cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### 3. Khởi chạy hệ thống
Chạy file `main.py` để bắt đầu phát hiện té ngã:
```bash
python main.py
```
*Nhấn phím `q` trên cửa sổ camera hiển thị để tắt hệ thống và dọn dẹp tài nguyên an toàn.*

## Luồng hoạt động của thuật toán (Logic)
Dự án giải quyết bài toán phát hiện ngã qua 3 bước kiểm chứng nghiêm ngặt để đảm bảo độ chính xác:
1. **YOLO Tracking:** Nhận diện người, gán Tracking ID cố định. Liên tục lưu lại và cập nhật tọa độ tâm (center) của bounding box.
2. **Tính vận tốc dọc (Y-axis Velocity):** Tính toán khoảng cách chênh lệch của tâm bounding box theo trục Y giữa 2 frame liên tiếp. Nếu tốc độ rơi vượt qua một ngưỡng nhất định (Threshold mặc định: > 50 pixel/giây), hệ thống sẽ bật cờ `high_drop_speed_detected`.
3. **Kiểm tra tư thế (MediaPipe Pose):** Hệ thống cắt (crop) riêng vùng ảnh chứa người đó và đưa qua MediaPipe để xác định tọa độ Y của 2 vai và 2 hông. Nếu trung bình tọa độ Y của vai lớn hơn Y của hông (nghĩa là vai đang ở vị trí gần mặt đất hơn hông), hệ thống bật cờ `is_fallen_posture`.
4. **Kết luận cuối cùng:** Trạng thái "Ngã" chỉ được xác nhận và kích hoạt chuông báo động khi **CẢ HAI** điều kiện (2) và (3) diễn ra đồng thời.
```
