# tetra_dashboard.py
import curses
import time
import os
import csv
from datetime import datetime, timedelta

LOG_FILE = "/opt/tetra/tetra_sessions.csv"
DISPLAY_DURATION = 30  # seconds


def load_recent_sessions(duration_seconds):
    now = datetime.now()
    sessions = []
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                start_time = datetime.strptime(row[0], "%d/%m/%Y %H:%M:%S")
                rssi = float(row[3])
                if now - start_time <= timedelta(seconds=duration_seconds):
                    sessions.append((start_time, rssi))
            except (ValueError, IndexError):
                continue
    return sessions


def determine_threat_level(sessions):
    if not sessions:
        return "NONE", 0, None
    
    rssi_values = [rssi for _, rssi in sessions]
    peak_rssi = max(rssi_values)
    recent_count = len(sessions)

    if peak_rssi > -35 and recent_count > 1:
        level = "VERY HIGH"
    elif peak_rssi > -42:
        level = "HIGH"
    elif peak_rssi > -50:
        level = "MEDIUM"
    elif peak_rssi > -65:
        level = "LOW"
    else:
        level = "NONE"

    last_detection = max(sessions, key=lambda x: x[0])[0]
    return level, peak_rssi, last_detection


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    while True:
        stdscr.clear()
        sessions = load_recent_sessions(DISPLAY_DURATION)
        level, peak_rssi, last_seen = determine_threat_level(sessions)

        stdscr.addstr(1, 2, f"Pi Eye TETRA Monitor")
        stdscr.addstr(3, 4, f"Threat Level: {level}")
        if peak_rssi:
            stdscr.addstr(5, 4, f"Peak RSSI: {peak_rssi:.1f} dBm")
        if last_seen:
            stdscr.addstr(6, 4, f"Last detection: {last_seen.strftime('%H:%M:%S')}")
        stdscr.addstr(8, 4, f"Signals in last {DISPLAY_DURATION}s: {len(sessions)}")

        stdscr.refresh()
        time.sleep(1)

if __name__ == "__main__":
    curses.wrapper(main)
