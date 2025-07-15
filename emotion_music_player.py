import cv2
from deepface import DeepFace
import pygame
import os
import time


pygame.mixer.init()


emotion_music_map = {
    'happy': 'songs/happy.mp3',
    'sad': 'songs/sad.mp3',
    'angry': 'songs/angry.mp3',
    'neutral': 'songs/neutral.mp3'
    }


cap = cv2.VideoCapture(0)
prev_emotion = None
last_prediction_time = 0
prediction_interval = 5  

def play_music(emotion):
    global prev_emotion
    if emotion != prev_emotion:
        prev_emotion = emotion
        pygame.mixer.music.stop()
        music_file = emotion_music_map.get(emotion.lower())
        if music_file and os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # Loop indefinitely

print("Press 'Q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break


    frame = cv2.flip(frame, 1)

   
    if time.time() - last_prediction_time >= prediction_interval:
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            dominant_emotion = result[0]['dominant_emotion']
            print("Detected Emotion:", dominant_emotion)
            play_music(dominant_emotion)
            last_prediction_time = time.time()
        except Exception as e:
            print("Emotion detection error:", e)

   
    display_text = f'Emotion: {prev_emotion}' if prev_emotion else "Detecting..."
    cv2.putText(frame, display_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Emotion Music Player", frame)

    if cv2.waitKey(1) & 0xFF in [ord('q'), ord('Q')]:
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()
pygame.quit()


