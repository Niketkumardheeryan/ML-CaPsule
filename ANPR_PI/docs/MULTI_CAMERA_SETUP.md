# Multi-Camera Setup Guide for 16GB Raspberry Pi 5

With **16GB RAM**, your Raspberry Pi 5 can easily handle **multiple camera streams** simultaneously.

## Maximum Camera Support

| Configuration | Max Cameras | Performance |
|---------------|-------------|-------------|
| **Pi 5 (4GB) + CPU** | 1-2 | Acceptable |
| **Pi 5 (8GB) + CPU** | 2-3 | Good |
| **Pi 5 (16GB) + CPU** | 3-4 | **Excellent** ✨ |
| **Pi 5 (4GB) + Hailo** | 2-3 | Good |
| **Pi 5 (8GB) + Hailo** | 4-5 | Excellent |
| **Pi 5 (16GB) + Hailo** | **6-8** | **Professional** 🚀 |

## Recommended Setup for 16GB System

### Scenario 1: Apartment Complex (Entry + Exit)

```yaml
io:
  multi_camera: true
  cameras:
    entry_gate:
      source: "rtsp://admin:pass@192.168.1.100:554/stream"
      camera_type: "in"
      enabled: true
    exit_gate:
      source: "rtsp://admin:pass@192.168.1.101:554/stream"
      camera_type: "out"
      enabled: true

inference:
  frame_skip: 2  # 16GB RAM handles double cameras well
  input_size: 640  # Full resolution
```

**Expected FPS:**
- CPU: 4-5 FPS per camera (8-10 total)
- Hailo: 25-30 FPS per camera (50-60 total)

---

### Scenario 2: Large Parking Lot (4 Cameras)

```yaml
io:
  multi_camera: true
  cameras:
    north_entry:
      source: "rtsp://admin:pass@192.168.1.100:554/stream"
      camera_type: "in"
      enabled: true
    south_entry:
      source: "rtsp://admin:pass@192.168.1.101:554/stream"
      camera_type: "in"
      enabled: true
    north_exit:
      source: "rtsp://admin:pass@192.168.1.102:554/stream"
      camera_type: "out"
      enabled: true
    south_exit:
      source: "rtsp://admin:pass@192.168.1.103:554/stream"
      camera_type: "out"
      enabled: true

inference:
  frame_skip: 3  # Balance performance across 4 cameras
  use_hailo: true  # Highly recommended for 4+ cameras
```

**Expected Performance (with Hailo):**
- 20-25 FPS per camera
- Total throughput: 80-100 FPS
- Latency: 40-60ms per detection

---

### Scenario 3: Professional Setup (6-8 Cameras)

**Requirements:**
- 16GB RAM ✅
- Hailo-8 accelerator ✅
- Gigabit Ethernet ✅
- SSD storage ✅

```yaml
io:
  multi_camera: true
  cameras:
    entry_1:
      source: "rtsp://admin:pass@192.168.1.100:554/stream"
      camera_type: "in"
      enabled: true
    entry_2:
      source: "rtsp://admin:pass@192.168.1.101:554/stream"
      camera_type: "in"
      enabled: true
    entry_3:
      source: "rtsp://admin:pass@192.168.1.102:554/stream"
      camera_type: "in"
      enabled: true
    exit_1:
      source: "rtsp://admin:pass@192.168.1.103:554/stream"
      camera_type: "out"
      enabled: true
    exit_2:
      source: "rtsp://admin:pass@192.168.1.104:554/stream"
      camera_type: "out"
      enabled: true
    exit_3:
      source: "rtsp://admin:pass@192.168.1.105:554/stream"
      camera_type: "out"
      enabled: true

inference:
  frame_skip: 2
  use_hailo: true
  input_size: 512  # Slightly smaller for 6+ cameras
```

**Expected Performance:**
- 15-20 FPS per camera
- Total throughput: 90-120 FPS
- RAM usage: ~2-3GB (plenty of headroom)

---

## Memory Usage Estimates

| Cameras | CPU Mode | Hailo Mode | Headroom (16GB) |
|---------|----------|------------|-----------------|
| **1 camera** | 400MB | 500MB | 15.5GB ✅ |
| **2 cameras** | 600MB | 800MB | 15.2GB ✅ |
| **3 cameras** | 800MB | 1.1GB | 14.9GB ✅ |
| **4 cameras** | 1.0GB | 1.5GB | 14.5GB ✅ |
| **6 cameras** | 1.5GB | 2.2GB | 13.8GB ✅ |
| **8 cameras** | 2.0GB | 3.0GB | 13GB ✅ |

**Conclusion:** With 16GB, you have **massive headroom** for multi-camera setups.

---

## Optimization Tips

### 1. Use Lower Resolution Streams

For cameras where you don't need full HD:

```yaml
cameras:
  side_camera:
    # Use substream (lower resolution) instead of mainstream
    source: "rtsp://admin:pass@192.168.1.100:554/substream"
    # Reduces bandwidth by 70% with minimal accuracy loss
```

### 2. Stagger Frame Processing

If you have many cameras, process them in rotation:

```python
# Already implemented in multi_camera_infer.py
# Each camera runs in separate thread with intelligent buffering
```

### 3. Dedicated Network

Use **Gigabit Ethernet** instead of WiFi:
- Lower latency
- More stable connections
- Supports 8+ HD camera streams

### 4. Monitor Resource Usage

```bash
# Real-time monitoring
watch -n 1 'free -h; echo "---"; ps aux | grep python | grep -v grep'

# Should show:
# Memory: 2-3GB used (out of 16GB)
# CPU: 200-400% (2-4 cores active)
```

---

## Firebase Gate Control with Multiple Cameras

### Independent Gates per Camera

```python
# Automatically handled by camera_type
cameras:
  entry_north:
    camera_type: "in"  # Opens entry gate
  exit_south:
    camera_type: "out"  # Opens exit gate
```

### Shared Gate (Multiple Cameras → One Gate)

All cameras open the same barrier (current setup):

```yaml
firebase:
  enabled: true
  auto_close_delay: 10
  # Single barrier controlled by all cameras
```

---

## Network Bandwidth Requirements

| Cameras | Resolution | FPS | Bandwidth | 16GB Impact |
|---------|-----------|-----|-----------|-------------|
| **1** | 1080p | 25 | 8 Mbps | None |
| **2** | 1080p | 25 | 16 Mbps | None |
| **4** | 1080p | 25 | 32 Mbps | None |
| **6** | 1080p | 25 | 48 Mbps | None |
| **8** | 720p | 25 | 40 Mbps | None |

**Recommendation:** Use Gigabit Ethernet (1000 Mbps) for 4+ cameras.

---

## Load Balancing (Advanced)

For 8+ cameras, consider **dual Raspberry Pi setup**:

```
┌─────────────────────┐
│ Pi 5 #1 (16GB)      │
│ - Cameras 1-4       │──┐
│ - Hailo-8           │  │
└─────────────────────┘  │
                         ├──> Central Firebase Database
┌─────────────────────┐  │
│ Pi 5 #2 (16GB)      │  │
│ - Cameras 5-8       │──┘
│ - Hailo-8           │
└─────────────────────┘
```

Both Pi units write to same Firebase barrier node.

---

## Troubleshooting Multi-Camera

### Camera Drops / Reconnects

```bash
# Add auto-reconnect (already implemented)
# Cameras auto-reconnect on connection loss
# Check logs: logs/plates.csv
```

### Uneven FPS Across Cameras

```yaml
# Increase frame_skip for specific cameras
cameras:
  busy_camera:
    frame_skip: 5  # Process less frequently
  quiet_camera:
    frame_skip: 2  # Process more frequently
```

### Memory Leaks

```bash
# Monitor over time
python3 -c "
import psutil
import time
while True:
    mem = psutil.virtual_memory()
    print(f'{time.ctime()}: {mem.percent}% ({mem.used/1e9:.1f}GB used)')
    time.sleep(60)
"

# With 16GB, memory should stay under 3-4GB even after days of running
```

---

## Deployment Example: 4-Camera Setup

```bash
# 1. Configure
nano configs/config.yaml

# 2. Test each camera individually
python -m src.video_infer --source "rtsp://...100:554/stream"
python -m src.video_infer --source "rtsp://...101:554/stream"
python -m src.video_infer --source "rtsp://...102:554/stream"
python -m src.video_infer --source "rtsp://...103:554/stream"

# 3. Run all together
python -m src.multi_camera_infer

# Expected output:
# 🚀 Starting multi-camera mode with 4 cameras
# 🎥 [entry_1] Camera started: rtsp://...
# 🎥 [entry_2] Camera started: rtsp://...
# 🎥 [exit_1] Camera started: rtsp://...
# 🎥 [exit_2] Camera started: rtsp://...
# Total FPS: 80-100 (with Hailo)
# Memory: 1.5GB / 16GB (plenty of headroom)
```

---

## Conclusion

Your **16GB Raspberry Pi 5** is perfectly suited for:
- ✅ 2-4 cameras (comfortable, CPU mode)
- ✅ 4-6 cameras (excellent, Hailo mode)
- ✅ 6-8 cameras (professional, Hailo mode)

The extra RAM provides:
- Better frame buffering
- Smoother multi-camera operation
- Room for future features
- No memory pressure

**You're all set for a professional multi-camera deployment!** 🎯
