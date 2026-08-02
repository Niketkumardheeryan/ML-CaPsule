"""
Cloudinary photo upload helper
Uploads car photos to Cloudinary cloud storage (free tier)
"""
import os
import cv2
import numpy as np
from datetime import datetime

try:
    import cloudinary
    import cloudinary.uploader
    from cloudinary.utils import cloudinary_url
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False

# Cloudinary credentials
CLOUDINARY_CONFIG = {
    "cloud_name": "dmia3iqeh",
    "api_key": "437237689967824",
    "api_secret": "1_BTfBDRRMotPzevPnPhsQ2LF9A",
}

if CLOUDINARY_AVAILABLE:
    cloudinary.config(**CLOUDINARY_CONFIG)


def upload_car_photo(frame, crop, plate_text, bbox):
    """
    Upload car photo to Cloudinary in background thread (no performance impact).
    
    Args:
        frame: Full frame (numpy array)
        crop: Cropped plate region (numpy array)
        plate_text: Detected plate text
        bbox: Bounding box [x1, y1, x2, y2]
    
    Returns:
        dict with 'full_url' and 'plate_url' if successful, None otherwise
    """
    if not CLOUDINARY_AVAILABLE:
        print("⚠️  Cloudinary not available (package not installed)")
        return None
    
    try:
        # Sanitize plate text for folder name
        plate_clean = "".join(c for c in plate_text if c.isalnum() or c in "-_")[:20]
        if not plate_clean:
            plate_clean = "UNKNOWN"
        
        # Create folder path: car_photos/YYYY-MM-DD/PLATE_NUMBER/
        date_str = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        folder_path = f"car_photos/{date_str}/{plate_clean}"
        
        results = {}
        
        # Upload full frame
        try:
            _, full_buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            full_result = cloudinary.uploader.upload(
                full_buffer.tobytes(),
                folder=folder_path,
                public_id=f"{timestamp}_full",
                resource_type="image",
                overwrite=False,
            )
            results['full_url'] = full_result.get('secure_url', full_result.get('url'))
            print(f"📸 Full frame uploaded: {results['full_url']}")
        except Exception as e:
            print(f"⚠️  Failed to upload full frame: {e}")
        
        # Upload cropped plate
        if crop.size > 0:
            try:
                _, crop_buffer = cv2.imencode('.jpg', crop, [cv2.IMWRITE_JPEG_QUALITY, 90])
                crop_result = cloudinary.uploader.upload(
                    crop_buffer.tobytes(),
                    folder=folder_path,
                    public_id=f"{timestamp}_plate",
                    resource_type="image",
                    overwrite=False,
                )
                results['plate_url'] = crop_result.get('secure_url', crop_result.get('url'))
                print(f"📸 Plate crop uploaded: {results['plate_url']}")
            except Exception as e:
                print(f"⚠️  Failed to upload plate crop: {e}")
        
        if results:
            print(f"✅ Photos uploaded successfully for {plate_text}")
        return results if results else None
        
    except Exception as e:
        print(f"⚠️  Cloudinary upload error: {e}")
        return None

