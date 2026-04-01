import cv2
import numpy as np
import time
from ultralytics import YOLO
import mediapipe as mp

class FallDetector:
    def __init__(self, model_path="yolov8n.pt", vel_threshold=50):
        # Khởi tạo YOLO
        self.model = YOLO(model_path)
        
        # Khởi tạo MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_draw = mp.solutions.drawing_utils
        
        # Biến trạng thái
        self.track_history = {}
        self.vel_threshold = vel_threshold

    @staticmethod
    def get_center(box):
        x1, y1, x2, y2 = box
        return np.array([(x1 + x2) / 2, (y1 + y2) / 2])

    def process_frame(self, frame):
        """Xử lý từng frame, trả về frame đã vẽ và cờ báo ngã"""
        current_time = time.time()
        any_fall_detected = False

        # Tracking với YOLO
        results = self.model.track(frame, persist=True, classes=[0], verbose=False)

        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)

            for box, track_id in zip(boxes, track_ids):
                x1, y1, x2, y2 = box
                bbox = (x1, y1, x2, y2)

                # Khởi tạo trạng thái cho người mới
                if track_id not in self.track_history:
                    self.track_history[track_id] = {
                        'prev_center': None,
                        'prev_time': current_time,
                        'high_drop_speed_detected': False,
                        'fall_confirmed': False
                    }

                state = self.track_history[track_id]
                center = self.get_center(bbox)

                # BƯỚC A: TÍNH VẬN TỐC RƠI (TRỤC Y)
                dt = current_time - state['prev_time']
                vertical_velocity = 0 

                if state['prev_center'] is not None and dt > 0:
                    dy_center = center[1] - state['prev_center'][1]
                    vertical_velocity = dy_center / dt

                state['prev_center'] = center
                state['prev_time'] = current_time

                if vertical_velocity > self.vel_threshold:
                    state['high_drop_speed_detected'] = True

                # BƯỚC B: MEDIA PIPE - KIỂM TRA TƯ THẾ
                person_crop = frame[y1:y2, x1:x2]
                is_fallen_posture = False

                if person_crop.size != 0:
                    rgb = cv2.cvtColor(person_crop, cv2.COLOR_BGR2RGB)
                    pose_result = self.pose.process(rgb)

                    if pose_result.pose_landmarks:
                        self.mp_draw.draw_landmarks(
                            person_crop, 
                            pose_result.pose_landmarks, 
                            self.mp_pose.POSE_CONNECTIONS
                        )
                        
                        lm = pose_result.pose_landmarks.landmark
                        shoulder_y = (lm[11].y + lm[12].y) / 2 
                        hip_y = (lm[23].y + lm[24].y) / 2      

                        if shoulder_y > (hip_y - 0.2):
                            is_fallen_posture = True

                frame[y1:y2, x1:x2] = person_crop

                # BƯỚC C: KẾT HỢP LOGIC & CẬP NHẬT GIAO DIỆN
                color = (0, 255, 0) # Xanh lá: Bình thường

                if is_fallen_posture and state['high_drop_speed_detected']:
                    color = (0, 0, 255) # Đỏ
                    state['fall_confirmed'] = True
                    any_fall_detected = True
                elif not is_fallen_posture:
                    color = (0, 255, 0)
                    state['fall_confirmed'] = False
                    state['high_drop_speed_detected'] = False

                # Vẽ khung và thông số
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                info_text = f"ID:{track_id} VelY:{vertical_velocity:.0f} Fall:{state['fall_confirmed']}"
                cv2.putText(frame, info_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        return frame, any_fall_detected
