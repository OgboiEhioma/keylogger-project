🔐 Advanced Keylogger (Local Testing Only)

⚠️For educational and local testing purposes only. Do not deploy or distribute without proper legal authorization. Unauthorized surveillance is illegal.

This Python-based advanced keylogger is designed for local system monitoring and learning. It captures keystrokes, active windows, clipboard data, screenshots, and Edge browser activity (including download history).

 📁 Features

- ✅ Keystroke logging (keys pressed)
- 📋 Clipboard monitoring
- 🖼️ Periodic screenshots (every 60 seconds)
- 🪟 Active window tracking
- 🌐 Microsoft Edge browser history + downloads
- 🕵️ Incognito mode detection (basic – logs absence of visited sites)
- 🔐 AES-256 encryption (Fernet) for logs
- 🧽 Log cleanup tool
- 🖥️ GUI log viewer (coming soon)


 🛠 Requirements

- Python 3.11+
- OS: Windows (tested)
- Modules:
  - `pynput`
  - `pyperclip`
  - `pyautogui`
  - `psutil`
  - `cryptography`
  - `pywin32`
  - `pillow`
  - `sqlite3` (built-in)
  - `tkinter` (for GUI)

Install dependencies with:

```bash
pip install pynput pyperclip pyautogui pillow psutil pywin32 cryptography
