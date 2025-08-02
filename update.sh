#!/bin/bash

echo "[*] Updating PiEye..."

# Ensure /opt/tetra/ exists
sudo mkdir -p /opt/tetra/
sudo cp tetra_*.py /opt/tetra/
sudo cp spotalert.py /usr/local/bin/

# Copy .service files
sudo cp tetra_monitor.service /etc/systemd/system/
sudo cp tetra_logger.service /etc/systemd/system/
sudo cp tetra_sdr_probe.service /etc/systemd/system/

# Set permissions
sudo chmod +x /opt/tetra/*.py
sudo chmod +x /usr/local/bin/spotalert.py

# Reload and restart services
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable tetra-monitor.service
sudo systemctl enable tetra-logger.service
sudo systemctl enable tetra_sdr_probe.service
sudo systemctl restart tetra-monitor.service
sudo systemctl restart tetra-logger.service
sudo systemctl restart tetra_sdr_probe.service

echo "[✓] Update complete."
