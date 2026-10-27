import cv2
from src.config import (
    COLOR_BG_DARK,
    COLOR_BORDER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    COLOR_ACCENT_GREEN,
    COLOR_ACCENT_AMBER
)


class TacticalHUD:
    @staticmethod
    def draw_overlay(frame, fps, fingers, gesture_label, log_count):
        h, w, _ = frame.shape
        overlay = frame.copy()

        # Panel Header Atas
        cv2.rectangle(overlay, (20, 20), (w - 20, 75), COLOR_BG_DARK, -1)
        # Panel Telemetri Kiri Bawah
        cv2.rectangle(overlay, (20, h - 145), (390, h - 20), COLOR_BG_DARK, -1)

        # Transparansi (Alpha Blending)
        cv2.addWeighted(overlay, 0.78, frame, 0.22, 0, frame)

        # Border Garis Tipis Presisi
        cv2.rectangle(frame, (20, 20), (w - 20, 75), COLOR_BORDER, 1)
        cv2.rectangle(frame, (20, h - 145), (390, h - 20), COLOR_BORDER, 1)

        # Teks Header
        cv2.putText(
            frame, "VISION_CORE // GESTURE TELEMETRY ENGINE",
            (36, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.52, COLOR_TEXT_PRIMARY, 1, cv2.LINE_AA
        )
        cv2.putText(
            frame, "PRESS [S] SAVE LOG   |   PRESS [Q] EXIT",
            (36, 63), cv2.FONT_HERSHEY_SIMPLEX, 0.40, COLOR_TEXT_MUTED, 1, cv2.LINE_AA
        )

        # Indikator FPS di Kanan Atas
        fps_text = f"FPS: {int(fps):02d}"
        cv2.putText(
            frame, fps_text,
            (w - 120, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.55, COLOR_ACCENT_GREEN, 1, cv2.LINE_AA
        )

        # Panel Telemetri Status Jari & Gestur
        status_color = COLOR_ACCENT_GREEN if sum(fingers) > 0 else COLOR_ACCENT_AMBER
        cv2.putText(
            frame, f"STATE : {gesture_label}",
            (36, h - 115), cv2.FONT_HERSHEY_SIMPLEX, 0.48, status_color, 1, cv2.LINE_AA
        )
        cv2.putText(
            frame, f"ARRAY : {fingers} (ACTIVE: {sum(fingers)}/5)",
            (36, h - 85), cv2.FONT_HERSHEY_SIMPLEX, 0.44, COLOR_TEXT_PRIMARY, 1, cv2.LINE_AA
        )
        cv2.putText(
            frame, f"SAVED EVENT LOGS : {log_count}",
            (36, h - 55), cv2.FONT_HERSHEY_SIMPLEX, 0.42, COLOR_TEXT_MUTED, 1, cv2.LINE_AA
        )

        # Visualisasi 5 Kotak Indikator Jari
        finger_names = ["THM", "IDX", "MID", "RNG", "PNK"]
        for i, val in enumerate(fingers):
            bx = 36 + (i * 65)
            by = h - 42
            box_color = COLOR_ACCENT_GREEN if val == 1 else COLOR_BORDER
            cv2.rectangle(frame, (bx, by), (bx + 52, by + 12), box_color, -1 if val == 1 else 1)
            cv2.putText(
                frame, finger_names[i],
                (bx + 10, by - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.33, COLOR_TEXT_MUTED, 1, cv2.LINE_AA
            )

        return frame