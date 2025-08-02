import time
import csv
import os
from datetime import datetime
import random

LOG_FILE = "/opt/tetra/tetra_sessions.csv"

def fake_detection():
    """
    Simulates a random TETRA detection event.
    Produces fake frequency, RSSI, and burst length.
    """
    if random.random() < 0.2:
        return {
            "frequency": random.choice([390.0, 390.2, 390.4, 390.6, 390.8]),
            "rssi": random.randint(-90, -40),
            "burst_length": random.uniform(0.1, 0.8)
        }
    else:
        return None

def init_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "frequency", "rssi", "burst_length"])

def log_detection(detection):
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            timestamp,
            detection["frequency"],
            detection["rssi"],
            round(detection["burst_length"], 2)
        ])
    print(f"[{timestamp}] Detected: {detection}")

def main():
    init_log()
    while True:
        detection = fake_detection()
        if detection:
            log_detection(detection)
        time.sleep(1)

if __name__ == "__main__":
    main()
