import subprocess
import sys

# --- Auto-install packages if not already installed ---
def auto_install(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for pkg in ["cv2", "numpy", "gtts", "pygame"]:
    try:
        if pkg == "cv2":
            import cv2
        else:
            __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", f"{'opencv-python' if pkg == 'cv2' else pkg}"])

# --- Now that everything is installed, import them properly ---
import cv2
import numpy as np
from gtts import gTTS
import pygame
import time

# --- Emotion Simulator ---
def analyze_emotion(frame):
    return np.random.choice(["happy", "confused", "bored", "engaged"])

# --- Response Generator ---
def generate_ai_response(emotion):
    responses = {
        "happy": "Great job! Let’s move to the next challenge!",
        "confused": "It seems like you’re stuck. Let me explain in a different way.",
        "bored": "Let’s make this fun! Here’s a cool example.",
        "engaged": "You’re doing amazing! Want a tougher challenge?"
    }
    return responses.get(emotion, "Keep going! You're learning fast!")

# --- Speak the Response ---
import uuid  # at the top of your script

def text_to_speech(text):
    filename = f"response_{uuid.uuid4().hex}.mp3"  # generate unique filename
    tts = gTTS(text)
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(1)
    
    try:
        import os
        os.remove(filename)  # clean up file after playing
    except Exception as e:
        print(f"Couldn't delete audio file: {e}")

# --- Main App ---
def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return
    
    print("👁️  AI Tutor running. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        emotion = analyze_emotion(frame)
        response = generate_ai_response(emotion)
        print(f"Detected: {emotion} → AI says: {response}")
        text_to_speech(response)
        
        cv2.imshow("AI Tutor - Press 'q' to exit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
