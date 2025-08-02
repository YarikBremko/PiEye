# spotalert.py
#!/usr/bin/env python3
import sys
import os
import csv
from datetime import datetime, timedelta

SIGHTING_FILE = "/opt/tetra/sightings.csv"

if len(sys.argv) < 3 or sys.argv[1] != "-t":
    print("Usage: spotalert -t <seconds_ago>")
    sys.exit(1)

try:
    seconds_ago = int(sys.argv[2])
    timestamp = datetime.now() - timedelta(seconds=seconds_ago)
    os.makedirs(os.path.dirname(SIGHTING_FILE), exist_ok=True)
    with open(SIGHTING_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp.strftime("%d/%m/%Y %H:%M:%S"), "Sighting"])
    print(f"✅ Logged sighting at {timestamp.strftime('%H:%M:%S')}")
except Exception as e:
    print("Error:", e)
    sys.exit(1)
