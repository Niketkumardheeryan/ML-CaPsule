# Hailo-8 Quick Start Guide

Deploy ANPR on Raspberry Pi 5 with Hailo-8 (13 TOPS) in under 30 minutes.

## Prerequisites

- Raspberry Pi 5 (4GB+ RAM)
- Hailo-8 M.2 HAT+ or HAT
- 32GB+ microSD with Raspberry Pi OS (64-bit)
- IP camera with RTSP stream

## Step 1: Hardware Setup (5 min)

```bash
# 1. Attach Hailo-8 M.2 HAT+ to Pi 5
#    - Align connector carefully
#    - Secure with provided screws

# 2. Boot Pi 5 and connect via SSH
ssh pi@raspberrypi.local
```

## Step 2: Install Hailo Runtime (10 min)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Hailo software
sudo apt install hailo-all -y

# Verify installation
hailortcli fw-control identify
# Expected: Device ID: 0000:01:00.0, Hailo-8

# Install Python bindings
pip3 install hailort
```

## Step 3: Clone and Setup Project (5 min)

```bash
# Clone repository
cd ~
git clone <your-repo-url> number-plate
cd number-plate

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_hailo.txt
```

## Step 4: Get Pre-compiled Models (5 min)

### Option A: Use Hailo Model Zoo (Fastest)

```bash
# Install Hailo Model Zoo
pip install hailo-model-zoo

# Download pre-compiled OCR model
hailomz get license_plate_ocr
cp ~/.hailomz/license_plate_ocr/*.hef models/ocr_crnn.hef

# Download YOLOv8 (optional, for full Hailo pipeline)
hailomz get yolov8n
cp ~/.hailomz/yolov8n/*.hef models/yolov8n.hef
```

### Option B: Use Provided Models

```bash
# Copy pre-compiled HEF files to Pi
# (from your development machine)
scp models/*.hef pi@raspberrypi.local:~/number-plate/models/
```

## Step 5: Configure System (3 min)

```bash
# Edit config
nano configs/config.yaml
```

Update these settings:

```yaml
models:
  ocr_backend: hailo
  ocr_hef: models/ocr_crnn.hef

inference:
  device: hailo
  use_hailo: true
  use_onnx: false
  frame_skip: 2  # Hailo is fast

io:
  multi_camera: true
  cameras:
    in:
      source: "rtsp://admin:password@192.168.1.108:554/stream"
      camera_type: "in"
      enabled: true

firebase:
  enabled: true
  auto_close_delay: 10
```

## Step 6: Test System (2 min)

```bash
# Test Firebase connection
python test_firebase.py

# Test gate control
python test_gate_multicamera_flow.py

# Test single camera (without gate)
python -m src.video_infer --source 0 --conf 0.25 --mode overlay
```

## Step 7: Run Production System

```bash
# Run multi-camera with gate control
python -m src.multi_camera_infer

# Expected output:
# 🚀 Using Hailo-8 accelerator for OCR
# ✅ Hailo OCR initialized - Input: 100x32
# 🚀 Starting multi-camera mode with 1 cameras
# 🎥 [in] Camera started: rtsp://admin:...
# FPS: 22-28
```

## Performance Monitoring

```bash
# In separate terminal
watch -n 1 'hailortcli monitor'

# Check system resources
htop

# Monitor logs
tail -f logs/plates.csv
```

## Troubleshooting

### Hailo Not Detected

```bash
# Check PCIe
lspci | grep Hailo
# Should show: 01:00.0 Co-processor: Hailo Technologies Ltd. Hailo-8

# Reinstall driver
sudo apt install --reinstall hailo-all
sudo reboot
```

### Low FPS

```bash
# Enable performance mode
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Check Hailo utilization
hailortcli monitor
# Power consumption should be 3-5W when processing
```

### Camera Connection Issues

```bash
# Test RTSP stream
ffplay rtsp://admin:password@192.168.1.108:554/stream

# Or use VLC
cvlc rtsp://admin:password@192.168.1.108:554/stream
```

## Auto-Start on Boot

```bash
# Create systemd service
sudo nano /etc/systemd/system/anpr.service
```

Paste this:

```ini
[Unit]
Description=ANPR with Hailo
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/number-plate
ExecStart=/home/pi/number-plate/venv/bin/python -m src.multi_camera_infer
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable anpr.service
sudo systemctl start anpr.service

# Check status
sudo systemctl status anpr.service
```

## Expected Performance

| Metric | Value |
|--------|-------|
| **Detection FPS** | 30-40 |
| **OCR Latency** | 8-10ms |
| **Total FPS** | 22-28 |
| **Power Draw** | 8-12W |
| **Accuracy** | 95%+ |

## Next Steps

- Fine-tune detection threshold in config.yaml
- Add more cameras (supports up to 4 streams)
- Train custom CRNN on your plate dataset
- Set up remote monitoring dashboard

## Support

- Hailo issues: https://hailo.ai/developer-zone/
- ANPR issues: Check main README.md
- Pi issues: https://forums.raspberrypi.com/

---

**Ready to deploy!** 🚀
