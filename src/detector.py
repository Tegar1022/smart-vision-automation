import cv2
import mediapipe as mp
from src.config import MAX_HANDS, DETECTION_CONFIDENCE, TRACKING_CONFIDENCE


class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_HANDS,
            min_detection_confidence=DETECTION_CONFIDENCE,
            min_tracking_confidence=TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]  # ID ujung jari: Jempol, Telunjuk, Tengah, Manis, Kelingking

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_frame)
        return self.results

    def extract_landmarks(self, frame):
        landmark_list = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            h, w, _ = frame.shape

            for idx, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmark_list.append((idx, cx, cy))

            # Gambar garis kerangka tangan dengan warna bersih
            self.mp_draw.draw_landmarks(
                frame,
                hand,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_draw.DrawingSpec(color=(240, 240, 240), thickness=1, circle_radius=2),
                self.mp_draw.DrawingSpec(color=(129, 185, 16), thickness=2, circle_radius=1)
            )
        return landmark_list

    def count_fingers(self, landmarks):
        if not landmarks:
            return [0, 0, 0, 0, 0]

        fingers = []

        # Logika Ibu Jari (cek sumbu X)
        if landmarks[self.tip_ids[0]][1] < landmarks[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Logika 4 Jari Lainnya (cek sumbu Y ujung jari terhadap sendi di bawahnya)
        for idx in range(1, 5):
            if landmarks[self.tip_ids[idx]][2] < landmarks[self.tip_ids[idx] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    @staticmethod
    def classify_gesture(fingers):
        total = sum(fingers)
        if total == 0:
            return "STANDBY // FIST"
        if fingers == [0, 1, 0, 0, 0]:
            return "CMD_01 // POINTER_ACTIVE"
        if fingers == [0, 1, 1, 0, 0]:
            return "CMD_02 // SNAPSHOT_LOG"
        if fingers == [0, 1, 1, 1, 0]:
            return "CMD_03 // SYSTEM_VERIFY"
        if total == 5:
            return "OPEN_PALM // SCANNING"
        return f"CUSTOM_STATE // {total}_FINGERS"