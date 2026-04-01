import time
import winsound
import threading

class AlarmSystem:
    def __init__(self):
        self.alarm_active = False
        self.thread = threading.Thread(target=self._play_alarm, daemon=True)
        self.thread.start()

    def _play_alarm(self):
        """Luồng âm thanh chạy ngầm"""
        while True:
            if self.alarm_active:
                winsound.Beep(1200, 500)
                time.sleep(0.1)  # Nghỉ 100ms
            else:
                time.sleep(0.1)  # Ngủ chờ nếu không có báo động

    def set_alarm(self, is_active: bool):
        """Bật/tắt trạng thái cảnh báo"""
        self.alarm_active = is_active

    def stop(self):
        """Dừng cảnh báo khi thoát chương trình"""
        self.alarm_active = False
