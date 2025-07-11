from cryptography.fernet import Fernet
import os

with open("secret.key", "rb") as f:
    cipher = Fernet(f.read())

output_file = "decrypted_log.txt"
with open(output_file, "w", encoding="utf-8") as outfile:
    for file in os.listdir("encrypted_logs"):
        if file.endswith(".enc"):
            path = os.path.join("encrypted_logs", file)
            with open(path, "rb") as f:
                data = cipher.decrypt(f.read()).decode("utf-8")
                outfile.write(data + "\n")

print(f"Decrypted log saved to {output_file}")
