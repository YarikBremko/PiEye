import curses
import csv
import time
import os
import socket

SESSION_FILE = "/opt/tetra/tetra_sessions.csv"

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "No IP"

def parse_sessions():
    now = time.time()
    window = 60  # Look at the past 60 seconds
    burst_count = 0
    peak_rssi = -100

    if not os.path.exists(SESSION_FILE):
        return 0, -100

    with open(SESSION_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                ts = time.strptime(row['timestamp'], "%H:%M:%S")
                current_time = time.localtime()
                row_time = time.mktime(current_time[:3] + ts[3:6] + current_time[6:])
                if now - row_time < window:
                    burst_count += 1
                    rssi = int(row.get("rssi", -100))
                    peak_rssi = max(peak_rssi, rssi)
            except:
                continue

    return burst_count, peak_rssi

def calculate_threat(burst_count, peak_rssi):
    if burst_count > 10 and peak_rssi >= -25:
        return "VERY HIGH"
    elif burst_count > 7 and peak_rssi >= -30:
        return "HIGH"
    elif peak_rssi >= -35 or burst_count > 4:
        return "MEDIUM"
    elif peak_rssi >= -40 or burst_count > 1:
        return "LOW"
    else:
        return "NONE"

def draw_dashboard(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    while True:
        stdscr.erase()

        ip = get_ip_address()
        burst_count, peak_rssi = parse_sessions()
        threat = calculate_threat(burst_count, peak_rssi)

        stdscr.addstr(1, 2, "📡 Pi Eye - Emergency Signal Monitor")
        stdscr.addstr(2, 2, f"Local IP: {ip}")
        stdscr.addstr(4, 4, f"Threat Level: {threat}")
        stdscr.addstr(5, 4, f"Recent bursts: {burst_count}")
        stdscr.addstr(6, 4, f"Peak RSSI: {peak_rssi} dB")
        stdscr.addstr(8, 2, f"Last update: {time.strftime('%H:%M:%S')}")

        stdscr.refresh()
        time.sleep(1)

def main():
    curses.wrapper(draw_dashboard)

if __name__ == "__main__":
    main()
