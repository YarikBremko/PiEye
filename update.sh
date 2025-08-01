#!/bin/bash
cd /home/yflik/pi-eye || exit 1
echo "📦 Pulling latest code from GitHub..."
git pull
sudo cp tetra_dashboard.py /opt/tetra/
sudo cp tetra_logger.py /opt/tetra/
sudo cp spotalert.py /usr/local/bin/spotalert
sudo chmod +x /usr/local/bin/spotalert
sudo systemctl restart tetra-monitor
echo "✅ Pi Eye updated successfully!"
