import os
import time
import csv
from datetime import datetime

LOG_FILE = "/opt/tetra/tetra_sessions.csv"

# Simulated detection input (replace with actual scanner integration)
def fake_detection():
    from random import uniform, randint
    return {
        "start": datetime.now(),
        "end": datetime.now(),
        "freq": 381.2,
        "rssi": uniform(-70, -30),
        "bursts": randint(1, 5),
        "service": "0x10"
    }

def log_detection(d):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            d["start"].strftime("%d/%m/%Y %H:%M:%S"),
            d["end"].strftime("%d/%m/%Y %H:%M:%S"),
            d["freq"],
            round(d["rssi"], 2),
            d["bursts"],
            d["service"]
        ])

if __name__ == "__main__":
    while True:
        detection = fake_detection()
        log_detection(detection)
        time.sleep(2)
