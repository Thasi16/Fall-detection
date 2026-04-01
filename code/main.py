import cv2
from fall_detector import FallDetector
from alert_system import AlarmSystem

def main():
    # Khởi tạo các module
    detector = FallDetector()
    alarm = AlarmSystem()
    
    cap = cv2.VideoCapture(0)

    print("Bắt đầu hệ thống phát hiện té ngã. Nhấn 'q' để thoát.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không thể kết nối với Camera.")
            break

        # Xử lý frame qua AI
        processed_frame, is_falling = detector.process_frame(frame)

        # Cập nhật trạng thái chuông báo
        alarm.set_alarm(is_falling)

        # Hiển thị
        cv2.imshow("Smart Fall Detection", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Dọn dẹp tài nguyên
    alarm.stop()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
