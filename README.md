## Fall-detection

Đây là phiên bản **README ngắn gọn**, chỉ tóm gọn phần quan trọng để giới thiệu dự án và cách chạy, vẫn đủ để người khác hiểu:

---

# Smart Fall Detection

A real-time human fall detection system using **YOLOv8** and **MediaPipe Pose**.
Detects sudden falls based on **motion speed + body posture** and triggers an alarm.

---

## Features

* Real-time human detection with YOLOv8
* Pose estimation with MediaPipe
* Fall detection using:

  * Vertical velocity (sudden drop)
  * Shoulder vs hip posture
* Multi-person tracking
* Alarm sound alert

---


## Usage

```bash
python main.py
```

Press **`q`** to quit.

---

## Detection Logic

```
Fall = Sudden Drop + Fallen Posture
```

* Sudden drop: vertical velocity exceeds threshold
* Fallen posture: shoulders lower than hips

---

## Author

Thái

---

Nếu muốn, mình có thể làm thêm **bản tiếng Việt cực ngắn gọn** nữa, chỉ tầm 10–12 dòng là xong, phù hợp để đưa trực tiếp lên GitHub.
Bạn có muốn mình làm luôn không?
