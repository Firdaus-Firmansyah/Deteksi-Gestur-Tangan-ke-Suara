import cv2
import mediapipe as mp
from gtts import gTTS
import os
import time
import pygame
from io import BytesIO

# Inisialisasi pygame mixer untuk memutar suara
pygame.mixer.init()

# Inisialisasi modul MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Inisialisasi webcam
# Turunkan resolusi kamera untuk mengurangi lag
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1040)  # Ubah resolusi menjadi 640x480
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 880) # Resolusi yang lebih rendah memproses lebih cepat

# Variabel untuk cooldown suara
last_speech_time = time.time()
speech_cooldown = 2  # Cooldown selama 2 detik
last_detected_state = None
speech_in_progress = False

# Fungsi untuk menghasilkan dan memutar suara
def speak(text):
    global speech_in_progress
    if speech_in_progress:
        return
        
    speech_in_progress = True
    
    try:
        mp3_fp = BytesIO()
        tts = gTTS(text=text, lang='id')
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
        pygame.mixer.music.load(mp3_fp)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error: Tidak dapat memutar audio. Detail: {e}")
        speech_in_progress = False
        return

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    mp3_fp.close()
    
    speech_in_progress = False

# Fungsi deteksi gestur
def get_hand_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark
    
    # Fungsi bantu untuk cek apakah jari ditekuk
    def is_finger_curled(tip_id, pip_id):
        return landmarks[tip_id].y > landmarks[pip_id].y

    # Fungsi bantu untuk cek apakah jari terbuka
    def is_finger_straight(tip_id, pip_id):
        return landmarks[tip_id].y < landmarks[pip_id].y
    
    # Jempol (THUMB) - logika berbeda karena posisinya horizontal
    is_thumb_straight = landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.THUMB_IP].x
    is_thumb_curled = not is_thumb_straight

    # Jari telunjuk (INDEX)
    is_index_straight = is_finger_straight(8, 6)
    is_index_curled = is_finger_curled(8, 6)

    # Jari tengah (MIDDLE)
    is_middle_straight = is_finger_straight(12, 10)
    is_middle_curled = is_finger_curled(12, 10)

    # Jari manis (RING)
    is_ring_straight = is_finger_straight(16, 14)
    is_ring_curled = is_finger_curled(16, 14)

    # Jari kelingking (PINKY)
    is_pinky_straight = is_finger_straight(20, 18)
    is_pinky_curled = is_finger_curled(20, 18)

    # === LOGIKA DETEKSI GESTUR ===
    
    # Peace Sign (V-sign)
    if is_index_straight and is_middle_straight and is_ring_curled and is_pinky_curled and is_thumb_curled:
        return "Peace Sign"
    
    # Shaka Sign
    elif is_index_curled and is_middle_curled and is_ring_curled and is_thumb_straight and is_pinky_straight:
        return "Shaka Sign"
        
    # OK Sign
    # Jari telunjuk dan jempol membentuk lingkaran
    elif is_middle_straight and is_ring_straight and is_pinky_straight and \
         abs(landmarks[mp_hands.HandLandmark.THUMB_TIP].y - landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y) < 0.05 and \
         abs(landmarks[mp_hands.HandLandmark.THUMB_TIP].x - landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x) < 0.05:
        return "OK Sign"
    
    # Rock On Sign
    elif is_thumb_curled and is_index_straight and is_middle_curled and is_ring_curled and is_pinky_straight:
        return "Rock On Sign"
    
    # Stop Sign (semua jari lurus)
    elif is_thumb_straight and is_index_straight and is_middle_straight and is_ring_straight and is_pinky_straight:
        return "Stop Sign"
    
    return "Tidak Ada"

# Loop utama untuk pemrosesan real-time
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Tidak bisa membaca frame dari kamera.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    current_state = "Tidak Ada"
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            current_state = get_hand_gesture(hand_landmarks)

    text_to_display = f"Status: {current_state}"
    cv2.putText(frame, text_to_display, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    current_time = time.time()
    
    if current_time - last_speech_time > speech_cooldown and not speech_in_progress:
        if current_state != "Tidak Ada" and current_state != last_detected_state:
            if current_state == "Peace Sign":
                speak("Hello")
            elif current_state == "Shaka Sign":
                speak("Perkenalkan")
            elif current_state == "OK Sign":
                speak("nama saya")
            elif current_state == "Rock On Sign":
                speak("Firdaus Firmansyah")
            elif current_state == "Stop Sign":
                speak("Terima kasih atas perhatiannya")
            
            last_detected_state = current_state
            last_speech_time = current_time

    cv2.imshow('Hand Recognition', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bersihkan resources
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()