import csv
import os
import time
from datetime import datetime
import cv2

from src.config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT
from src.detector import HandDetector
from src.hud import TacticalHUD

LOG_FILE = os.path.join("logs", "gesture_events.csv")


def append_event_log(gesture_label, fingers):
    os.makedirs("logs", exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "gesture", "finger_array", "active_count"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            gesture_label,
            str(fingers),
            sum(fingers)
        ])


def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():
        print("[error] Kamera tidak terdeteksi. Pastikan webcam aktif.")
        return

    detector = HandDetector()
    hud = TacticalHUD()

    prev_time = 0
    log_count = 0

    print("[vision] Smart Vision Engine berjalan. Tekan 'q' pada jendela kamera untuk keluar.")

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Flip horizontal agar seperti cermin
        frame = cv2.flip(frame, 1)

        # Deteksi tangan & jari
        detector.process_frame(frame)
        landmarks = detector.extract_landmarks(frame)
        fingers = detector.count_fingers(landmarks) if landmarks else [0, 0, 0, 0, 0]
        gesture_label = detector.classify_gesture(fingers) if landmarks else "NO_HAND_DETECTED"

        # Hitung FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
        prev_time = curr_time

        # Render Tactical HUD
        frame = hud.draw_overlay(frame, fps, fingers, gesture_label, log_count)

        cv2.imshow("SMART_VISION_CORE // Telemetry Monitor", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            append_event_log(gesture_label, fingers)
            log_count += 1
            print(f"[log] Event disimpan: {gesture_label} -> {fingers}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()