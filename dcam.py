import argparse
import os
import sys
import urllib.request
import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils, HandLandmarksConnections

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(SCRIPT_DIR, "models")

GESTURE_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"
SEGMENTER_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_segmenter/float16/latest/selfie_segmenter.tflite"


def ensure_model(filename: str, url: str) -> str:
    """Memastikan file model MediaPipe sudah terdownload secara lokal."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    filepath = os.path.join(MODELS_DIR, filename)
    if not os.path.exists(filepath):
        print(f"[INFO] Mendownload model MediaPipe: {filename}...")
        urllib.request.urlretrieve(url, filepath)
        print(f"[SUCCESS] Model {filename} berhasil didownload.")
    return filepath


# Coba import pyvirtualcam (opsional, agar bisa langsung terbaca sebagai webcam di Discord)
try:
    import pyvirtualcam
    HAS_VIRTUALCAM = True
except ImportError:
    HAS_VIRTUALCAM = False
    print("[INFO] 'pyvirtualcam' belum terinstall. Berjalan dalam mode Window biasa.")
    print("       Tips: Install OBS Studio + 'pip install pyvirtualcam' agar langsung muncul di daftar kamera Discord!\n")


def is_peace_sign(hand_landmarks):
    lm = hand_landmarks.landmark if hasattr(hand_landmarks, "landmark") else hand_landmarks

    index_up = lm[8].y < lm[6].y
    middle_up = lm[12].y < lm[10].y

    # Jari manis dan kelingking harus ditekuk (TIP berada di bawah PIP)
    ring_down = lm[16].y > lm[14].y
    pinky_down = lm[20].y > lm[18].y

    return index_up and middle_up and ring_down and pinky_down


def init_webcam(camera_index: int = 0, target_width: int = 1280, target_height: int = 720):
    if os.name == "nt":
        print(f"[INFO] Membuka kamera {camera_index} via DirectShow (CAP_DSHOW)...")
        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, target_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, target_height)
        if cap.isOpened():
            ret, test_frame = cap.read()
            if ret and test_frame is not None:
                actual_h, actual_w = test_frame.shape[:2]
                print(f"[SUCCESS] Kamera aktif: {actual_w}x{actual_h}")
                return cap, actual_w, actual_h
            cap.release()

    print(f"[INFO] Membuka kamera {camera_index} via default backend...")
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, target_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, target_height)
    if cap.isOpened():
        ret, test_frame = cap.read()
        if ret and test_frame is not None:
            actual_h, actual_w = test_frame.shape[:2]
            print(f"[SUCCESS] Kamera aktif: {actual_w}x{actual_h}")
            return cap, actual_w, actual_h
        cap.release()

    return None, 0, 0


def main():
    parser = argparse.ArgumentParser(description="Discord Meme Cam ADIOS")
    parser.add_argument("--camera", "-c", type=int, default=0, help="Index kamera (default: 0)")
    parser.add_argument("--width", type=int, default=1280, help="Lebar frame (default: 1280)")
    parser.add_argument("--height", type=int, default=720, help="Tinggi frame (default: 720)")
    parser.add_argument("--fps", type=int, default=30, help="FPS kamera (default: 30)")
    parser.add_argument("--fade-out-speed", type=float, default=0.15, help="Kecepatan memudar/menghilang (default: 0.15)")
    parser.add_argument("--fade-in-speed", type=float, default=0.15, help="Kecepatan muncul kembali (default: 0.15)")
    parser.add_argument("--no-flip", action="store_true", help="Jangan balik/cerminkan frame horizontal")
    args = parser.parse_args()

    cap, width, height = init_webcam(args.camera, args.width, args.height)
    if cap is None:
        print(f"\n[ERROR] Tidak dapat membuka kamera pada index {args.camera}.")
        print("Saran penyelesaian:")
        print("  1. Pastikan webcam tidak sedang digunakan oleh aplikasi lain (Discord, Zoom, Browser, dll).")
        print("  2. Coba ganti index kamera, misalnya: python dcam.py --camera 1")
        sys.exit(1)

    fps = args.fps

    print("[INFO] Memuat model MediaPipe Tasks...")
    gesture_model_path = ensure_model("gesture_recognizer.task", GESTURE_MODEL_URL)
    segmenter_model_path = ensure_model("selfie_segmenter.tflite", SEGMENTER_MODEL_URL)

    gest_base = python.BaseOptions(model_asset_path=gesture_model_path)
    gest_options = vision.GestureRecognizerOptions(base_options=gest_base, num_hands=2)
    recognizer = vision.GestureRecognizer.create_from_options(gest_options)

    seg_base = python.BaseOptions(model_asset_path=segmenter_model_path)
    seg_options = vision.ImageSegmenterOptions(base_options=seg_base, output_confidence_masks=True)
    segmenter = vision.ImageSegmenter.create_from_options(seg_options)

    background_frame = None
    alpha = 1.0  
    fade_out_speed = args.fade_out_speed  
    fade_in_speed = args.fade_in_speed   
    show_hud = True        
    mirror = not args.no_flip 
    print("==========================================")
    print("   DISKORT ADIOS!   ")
    print("==========================================")
    print("Key:")
    print("  [b] : Ambil ulang foto background kosong (minggir dulu dari kamera)")
    print("  [m] : Toggle Mirror (on/off)")
    print("  [h] : show/hide teks")
    print("  [q] : close/quit")
    print("==========================================")

    vcam = None
    if HAS_VIRTUALCAM:
        try:
            vcam = pyvirtualcam.Camera(width=width, height=height, fps=fps, fmt=pyvirtualcam.PixelFormat.BGR)
            print(f"[SUCCESS] Virtual Camera aktif di: {vcam.device}")
        except Exception as e:
            print(f"[WARNING] Gagal mengaktifkan Virtual Camera ({e}). Pastikan OBS Virtual Camera sudah terinstall.")
            vcam = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Gagal membaca frame dari webcam.")
            break

        if mirror:
            frame = cv2.flip(frame, 1)

        if background_frame is None:
            background_frame = frame.copy()

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        gest_results = recognizer.recognize(mp_image)
        peace_detected = False

        if gest_results.gestures:
            for gesture_list in gest_results.gestures:
                for gesture in gesture_list:
                    if gesture.category_name.lower() in ("victory", "peace"):
                        peace_detected = True

        if gest_results.hand_landmarks:
            for hand_lms in gest_results.hand_landmarks:
                if is_peace_sign(hand_lms):
                    peace_detected = True
                if show_hud:
                    drawing_utils.draw_landmarks(frame, hand_lms, HandLandmarksConnections.HAND_CONNECTIONS)

        if peace_detected:
            alpha = max(0.0, alpha - fade_out_speed) 
        else:
            alpha = min(1.0, alpha + fade_in_speed)   

        if alpha < 0.99:
            seg_results = segmenter.segment(mp_image)
            raw_mask = seg_results.confidence_masks[0].numpy_view()

            mask = (raw_mask > 0.5).astype(np.float32)
            if mask.shape[:2] != frame.shape[:2]:
                mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
            if mask.ndim == 2:
                mask = mask[..., None]
            if mask.shape[-1] == 1:
                mask = np.repeat(mask, 3, axis=-1)
            mask = cv2.GaussianBlur(mask, (21, 21), 0)

            person_faded = cv2.addWeighted(frame, alpha, background_frame, 1.0 - alpha, 0)
            output_frame = (person_faded * mask + background_frame * (1.0 - mask)).astype(np.uint8)
        else:
            output_frame = frame.copy()

        if vcam is not None:
            vcam.send(output_frame)
            vcam.sleep_until_next_frame()

        preview_frame = output_frame.copy()
        if show_hud:
            status_text = "STATUS: MENGHILANG (PEACE OUT!)" if peace_detected else "STATUS: NORMAL"
            color = (0, 255, 255) if peace_detected else (0, 255, 0)
            cv2.putText(preview_frame, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.putText(
                preview_frame,
                f"Opacity: {int(alpha * 100)}% | [B] BG | [M] Flip:{'ON' if mirror else 'OFF'} | [H] HUD | [Q] Quit",
                (20, height - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

        cv2.imshow("Discord Vanish Cam (Preview)", preview_frame)

        # Kontrol Keyboard
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('b'):
            ret_bg, clean_bg = cap.read()
            if ret_bg:
                background_frame = cv2.flip(clean_bg, 1) if mirror else clean_bg.copy()
                print("[INFO] Background kosong berhasil diperbarui!")
        elif key == ord('m'):
            mirror = not mirror
            if background_frame is not None:
                background_frame = cv2.flip(background_frame, 1)
            print(f"[INFO] Mirror/Flip horizontal: {'AKTIF' if mirror else 'NONAKTIF'}")
        elif key == ord('h'):
            show_hud = not show_hud

    cap.release()
    recognizer.close()
    segmenter.close()
    if vcam is not None:
        vcam.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
