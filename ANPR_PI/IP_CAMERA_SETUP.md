# IP Camera Setup Guide for Multi-Camera ANPR System

This guide explains how to set up IP cameras for the multi-camera ANPR system with Firebase gate control.

## Table of Contents
- [Overview](#overview)
- [IP Camera Connection Methods](#ip-camera-connection-methods)
- [Configuration](#configuration)
- [Camera Types](#camera-types)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## Overview

The system supports two camera types:
- **Entry Camera (IN)**: Detects vehicles entering, opens entry gate (gate1)
- **Exit Camera (OUT)**: Detects vehicles leaving, opens exit gate (gate2)

When a valid license plate (matched in database) is detected:
- Entry camera → Opens gate1 (entry gate)
- Exit camera → Opens gate2 (exit gate)

## IP Camera Connection Methods

### 1. RTSP Stream (Recommended)

**Format:**
```
rtsp://username:password@ip_address:port/stream_path
```

**Examples:**
```yaml
# Hikvision camera
rtsp://admin:password123@192.168.1.100:554/Streaming/Channels/101

# Dahua camera
rtsp://admin:password123@192.168.1.101:554/cam/realmonitor?channel=1&subtype=0

# Generic RTSP
rtsp://admin:password123@192.168.1.102:554/stream1
```

**Common RTSP Ports:**
- Port 554 (default RTSP)
- Port 8554 (alternate)
- Port 10554 (some manufacturers)

### 2. HTTP Stream (MJPEG/HLS)

**Format:**
```
http://username:password@ip_address:port/path/to/stream
```

**Examples:**
```yaml
# MJPEG stream
http://admin:password123@192.168.1.100:8080/video

# HLS stream
http://admin:password123@192.168.1.100:8080/stream.m3u8
```

### 3. USB Camera (Device ID)

For local USB cameras, use device ID:
```yaml
source: 0  # First USB camera
source: 1  # Second USB camera
```

### 4. Video File

For testing, you can use video files:
```yaml
source: "path/to/video.mp4"
```

## Configuration

### Step 1: Update `config.yaml`

Edit `configs/config.yaml`:

```yaml
io:
  # Enable multi-camera mode
  multi_camera: true
  
  cameras:
    in:  # Entry camera
      source: "rtsp://admin:password123@192.168.1.100:554/Streaming/Channels/101"
      camera_type: "in"  # Must be "in" for entry
      enabled: true
    
    out:  # Exit camera
      source: "rtsp://admin:password123@192.168.1.101:554/Streaming/Channels/101"
      camera_type: "out"  # Must be "out" for exit
      enabled: true

# Firebase gate control
firebase:
  enabled: true
  auto_close_delay: 10  # Auto-close gate after 10 seconds (0 to disable)
```

### Step 2: Set Up Firebase Credentials

Create a `.env` file in the project root:

```env
FIREBASE_PRIVATE_KEY_ID=your_private_key_id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your-service-account@project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your_client_id
FIREBASE_CLIENT_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40project.iam.gserviceaccount.com
```

### Step 3: Install Dependencies

```bash
pip install firebase-admin opencv-python yaml
```

## Camera Types

### Entry Camera (IN)
- **Purpose**: Detect vehicles entering the parking area
- **Gate Control**: Opens `gate1` (entry gate) when valid plate detected
- **Session Log**: Records `entry_time` in session CSV

### Exit Camera (OUT)
- **Purpose**: Detect vehicles leaving the parking area
- **Gate Control**: Opens `gate2` (exit gate) when valid plate detected
- **Session Log**: Records `exit_time` in session CSV

## Running the System

### Multi-Camera Mode

```bash
python -m src.multi_camera_infer
```

### Single Camera Mode (Legacy)

```bash
python -m src.video_infer --source 0
```

## Finding Your Camera's RTSP URL

### Method 1: Camera Web Interface
1. Access camera web interface: `http://ip_address`
2. Login with admin credentials
3. Navigate to: **Settings → Network → RTSP**
4. Copy the RTSP URL

### Method 2: Manufacturer Default Paths

**Hikvision:**
```
rtsp://username:password@ip:554/Streaming/Channels/101  # Main stream
rtsp://username:password@ip:554/Streaming/Channels/102  # Sub stream
```

**Dahua:**
```
rtsp://username:password@ip:554/cam/realmonitor?channel=1&subtype=0  # Main
rtsp://username:password@ip:554/cam/realmonitor?channel=1&subtype=1  # Sub
```

**Axis:**
```
rtsp://username:password@ip/axis-media/media.amp
```

**Generic/ONVIF:**
```
rtsp://username:password@ip:554/stream1
rtsp://username:password@ip:554/h264
```

### Method 3: ONVIF Device Manager
1. Download ONVIF Device Manager (free tool)
2. Scan your network for cameras
3. View RTSP URLs in the tool

### Method 4: VLC Media Player Test
1. Open VLC → Media → Open Network Stream
2. Try common RTSP URLs
3. If stream opens, use that URL

## Testing

### Test Camera Connection

```python
import cv2

# Test RTSP stream
cap = cv2.VideoCapture("rtsp://admin:password@192.168.1.100:554/stream1")

if cap.isOpened():
    print("✅ Camera connected!")
    ret, frame = cap.read()
    if ret:
        print(f"Frame size: {frame.shape}")
        cv2.imshow("Test", frame)
        cv2.waitKey(0)
else:
    print("❌ Camera connection failed")
```

### Test Firebase Connection

```python
from src.firebase_gate import get_firebase_control

firebase = get_firebase_control()
if firebase.is_connected():
    print("✅ Firebase connected!")
    # Test gate control
    firebase.open_entry_gate()
    time.sleep(2)
    firebase.close_entry_gate()
else:
    print("❌ Firebase not connected")
```

## Troubleshooting

### Camera Connection Issues

**Problem: Camera not connecting**

**Solutions:**
1. Check IP address: `ping 192.168.1.100`
2. Check credentials (username/password)
3. Verify RTSP port (usually 554)
4. Check camera RTSP is enabled in settings
5. Test with VLC media player first
6. Try HTTP stream instead of RTSP
7. Check firewall/network settings

**Problem: High latency/delay**

**Solutions:**
```python
# Already implemented - buffer size reduced for RTSP
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
```

Reduce frame skip in config:
```yaml
inference:
  frame_skip: 1  # Process every frame (was 3)
```

**Problem: Camera disconnects frequently**

**Solutions:**
1. Use sub-stream (lower resolution) instead of main stream
2. Increase camera timeout settings
3. Check network stability
4. Use wired connection instead of WiFi

### Firebase Connection Issues

**Problem: Firebase not connecting**

**Solutions:**
1. Check `.env` file exists in project root
2. Verify all Firebase credentials are correct
3. Check private key format (must have `\n` for newlines)
4. Verify service account has database permissions
5. Check internet connection

**Problem: Gate not opening**

**Solutions:**
1. Verify plate is in `shobha_permanent_parking.csv`
2. Check Firebase connection status
3. Verify gate paths: `/gate1` and `/gate2`
4. Check Firebase Realtime Database rules allow writes
5. Monitor console for gate control messages

### Common Error Messages

**"Failed to open camera"**
- Check camera URL/credentials
- Verify camera is online
- Test with VLC first

**"Firebase not connected"**
- Check `.env` file
- Verify credentials
- Check internet connection

**"Gate control disabled"**
- Firebase credentials missing
- Service account lacks permissions

## Security Notes

1. **Never commit `.env` file** - Contains sensitive credentials
2. **Use strong passwords** for IP cameras
3. **Change default credentials** on all cameras
4. **Restrict camera network access** (firewall/VLAN)
5. **Use HTTPS/RTSP over VPN** if accessing remotely

## Network Requirements

- **Bandwidth**: ~1-2 Mbps per camera (for sub-stream)
- **Latency**: < 100ms recommended for real-time
- **Protocols**: RTSP (TCP/UDP), HTTP (TCP)
- **Ports**: 554 (RTSP), 8080 (HTTP), camera-specific ports

## Example Configurations

### Local USB Cameras
```yaml
cameras:
  in:
    source: 0  # First USB camera
    camera_type: "in"
    enabled: true
  out:
    source: 1  # Second USB camera
    camera_type: "out"
    enabled: true
```

### Mixed Setup (USB + IP)
```yaml
cameras:
  in:
    source: "rtsp://admin:pass@192.168.1.100:554/stream1"
    camera_type: "in"
    enabled: true
  out:
    source: 0  # USB camera for exit
    camera_type: "out"
    enabled: true
```

### Single Camera (Entry Only)
```yaml
cameras:
  in:
    source: "rtsp://admin:pass@192.168.1.100:554/stream1"
    camera_type: "in"
    enabled: true
  out:
    enabled: false  # Disable exit camera
```

## Firebase Database Structure

The system writes to Firebase Realtime Database:

```
/
  gate1: true/false  (Entry gate status)
  gate2: true/false  (Exit gate status)
```

**Gate Control:**
- `true` = Gate open
- `false` = Gate closed

**Auto-close:** Gates automatically close after `auto_close_delay` seconds (configurable).

## Support

For issues:
1. Check camera connection with VLC
2. Test Firebase with test script
3. Check logs in console output
4. Verify config.yaml syntax
5. Ensure all dependencies installed

