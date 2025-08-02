import subprocess
import time
import csv
from datetime import datetime
import os

OUTPUT_FILE = "/opt/tetra/tetra_sdr_probe.csv"
MIN_DB_THRESHOLD = -45  # Adjust based on your SDR's noise floor

def init_log():
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "frequency", "power_dB"])

def run_rtl_power():
    try:
        result = subprocess.run([
            "rtl_power",
            "-f", "390M:395M:12.5k",
            "-i", "1",
            "-g", "30"
        ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=5)

        lines = result.stdout.decode().splitlines()
        return [line for line in lines if not line.startswith("#")]

    except Exception as e:
        print(f"Error: {e}")
        return []

def parse_and_log(lines):
    timestamp = datetime.now().strftime("%H:%M:%S")
    for line in lines:
        parts = line.strip().split(",")
        if len(parts) < 7:
            continue
        start_freq = float(parts[0])
        bin_width = float(parts[2])
        db_values = list(map(float, parts[6:]))

        for i, db in enumerate(db_values):
            freq = start_freq + (i * bin_width)
            if db >= MIN_DB_THRESHOLD:
                with open(OUTPUT_FILE, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([timestamp, round(freq, 4), db])
                print(f"[{timestamp}] Peak: {round(freq, 4)} MHz @ {db} dB")

def main():
    init_log()
    while True:
        lines = run_rtl_power()
        parse_and_log(lines)
        time.sleep(1)

if __name__ == "__main__":
    main()
