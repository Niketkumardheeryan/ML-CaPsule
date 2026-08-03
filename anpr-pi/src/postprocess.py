import re
import csv
import os
from typing import Tuple, List, Optional
from difflib import SequenceMatcher

CONFUSION_MAP = {
    '0': 'O', 'O': '0',
    '1': 'I', 'I': '1',
    '8': 'B', 'B': '8',
    '5': 'S', 'S': '5',
    # W-specific misdetections
    '4': 'W', 'W': '4',  # W often misread as 4
    'N': 'W',  # W sometimes misread as N (but N->W only, not reverse)
    'I': 'W',  # W sometimes misread as I (but I->W only, not reverse)
}

# State code confusion map - common OCR misdetections
STATE_CODE_FIXES = {
    'TH': 'TN',  # Most common: TH detected as TN
    'TK': 'TN',
    'TM': 'TN',
    'IN': 'TN',
    'IH': 'TN',
    'IL': 'TN',
    'TR': 'TN',
    'TA': 'TN',
}

# Common state codes (priority order)
COMMON_STATE_CODES = ['TN', 'KL']

DEFAULT_PATTERNS = [
    r'^[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{3,4}$',
    r'^[A-Z]{2}[0-9]{2}[A-Z]{0,2}[0-9]{4}$',
    r'^[A-Z]{2}[0-9]{1,2}[A-Z][0-9]{4}$',
]


def normalize(raw_text: str) -> str:
    s = (raw_text or "").upper()
    s = re.sub(r'[^A-Z0-9]', '', s)
    return s


def quick_reject(text: str) -> bool:
    """
    Quick check to reject obviously non-plate text before expensive processing.
    Returns True if text should be REJECTED (not a plate).
    """
    if not text or len(text) < 6:  # Plates are at least 6 chars
        return True
    
    # Reject pure letters (no digits) - plates MUST have numbers
    if text.isalpha():
        return True
    
    # Reject pure numbers (no letters) - plates MUST have state code
    if text.isdigit():
        return True
    
    # Reject if no digits at all (plates must have registration numbers)
    if not any(c.isdigit() for c in text):
        return True
    
    # Reject if too long (Indian plates max ~10 chars)
    if len(text) > 12:
        return True
    
    # Reject common false positives (signage text)
    false_positives = ['CANTEEN', 'PARKING', 'ENTRY', 'EXIT', 'STOP', 'SLOW', 
                       'GATE', 'OPEN', 'CLOSE', 'NEEN', 'MEEN', 'JEEN', 'NMEEN', 'NTEEN', 'TEEN']
    text_upper = text.upper()
    for fp in false_positives:
        if fp in text_upper:
            return True
    
    return False


def fix_state_code(text: str) -> str:
    """Fix common state code misdetections, especially TN/TH confusion."""
    if not text or len(text) < 2:
        return text
    
    # Check first 2 chars for state code
    state_code = text[:2]
    if state_code in STATE_CODE_FIXES:
        return STATE_CODE_FIXES[state_code] + text[2:]
    return text


def confusion_correct(text: str) -> str:
    # Context-aware: letters region then numbers region heuristic for Indian plates
    if not text:
        return text
    chars = list(text)
    original_chars = chars.copy()  # Keep original for position 5 check
    # Heuristic: first 2 are letters, next 1-2 digits, next 1-2 letters, last 3-4 digits
    for i, ch in enumerate(chars):
        if ch not in CONFUSION_MAP:
            continue
        mapped = CONFUSION_MAP[ch]
        # decide mapping direction based on index groups
        if i in (0, 1):  # should be letters
            if ch.isdigit():
                chars[i] = mapped if mapped.isalpha() else chars[i]
        elif i in (2, 3):  # often digits
            if ch.isalpha():
                chars[i] = mapped if mapped.isdigit() else chars[i]
        elif i == 4:  # First letter position after district - ALWAYS convert if digit
            if ch.isdigit():
                chars[i] = mapped if mapped.isalpha() else chars[i]
            # Don't auto-convert N/I to W - let database matching handle it
            # (N and I are valid letters, database matching will correct if needed)
        elif i == 5:  # Could be letter OR first digit - be more careful
            # Only convert if it looks like a misread letter (not if it's clearly part of number sequence)
            # Check ORIGINAL previous char (before conversion) - if it was originally a LETTER, this might be letter too
            # If position 4 was originally a DIGIT, then position 5 is definitely part of the number sequence
            if ch.isdigit() and i > 0:
                prev_original = original_chars[i-1]
                # Only convert if previous was ORIGINALLY a letter (not a digit we converted)
                # If previous was a digit, then this is definitely part of the number sequence
                if prev_original.isalpha():
                    # Previous was originally a letter, this might be letter too (e.g., "AB" -> "A1" misread)
                    chars[i] = mapped if mapped.isalpha() else chars[i]
                # Otherwise leave it as digit (it's part of the number sequence)
        else:  # tail mostly digits
            if ch.isalpha():
                chars[i] = mapped if mapped.isdigit() else chars[i]
    return ''.join(chars)


def validate(text: str) -> Tuple[bool, str]:
    # Quick reject obviously non-plate text
    if quick_reject(text):
        return False, ""
    
    t = normalize(text)
    t = confusion_correct(t)
    t = fix_state_code(t)  # Fix state code misdetections
    # Don't do aggressive W conversion - let database matching handle it with 1-2 char tolerance
    for pat in DEFAULT_PATTERNS:
        if re.fullmatch(pat, t):
            return True, t
    return False, t


def validate_with_state_priority(text: str, original_text: Optional[str] = None) -> Tuple[bool, str]:
    """
    Validate text - just use regular validation with state code fixes.
    The TN/KL priority check was removed as it caused incorrect conversions.
    Returns (is_valid, corrected_text)
    """
    # Just use the regular validate function - it already handles state code fixes
    return validate(text)


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def similarity_ratio(s1: str, s2: str) -> float:
    """Calculate similarity ratio between two strings (0-1)."""
    return SequenceMatcher(None, s1, s2).ratio()


def load_permanent_parking_db(csv_path: str) -> dict:
    """
    Load vehicle numbers from permanent parking CSV.
    Returns dict mapping vehicle_number -> {'id': permanent_parking_id, 'vehicle_number': vehicle_number}
    """
    if not os.path.exists(csv_path):
        return {}
    
    db_dict = {}
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                vehicle_num = row.get('vehicle_number', '').strip().upper()
                parking_id = row.get('id', '').strip()
                if vehicle_num:
                    db_dict[vehicle_num] = {
                        'id': parking_id,
                        'vehicle_number': vehicle_num
                    }
    except Exception as e:
        print(f"Error loading permanent parking DB: {e}")
    
    return db_dict


def find_matching_plate(detected_plate: str, db_dict: dict, max_distance: int = 2) -> Optional[dict]:
    """
    Find matching plate in database with 1-2 char tolerance.
    Returns dict with 'id' and 'vehicle_number' if found, None otherwise.
    """
    detected_plate = normalize(detected_plate)
    detected_plate = fix_state_code(detected_plate)
    detected_len = len(detected_plate)
    
    best_match = None
    best_distance = max_distance + 1
    best_ratio = 0.0
    
    for db_plate, db_data in db_dict.items():
        db_plate_norm = normalize(db_plate)
        
        # Exact match - fast path
        if detected_plate == db_plate_norm:
            return db_data
        
        # Quick length check - skip if length difference > max_distance
        if abs(len(db_plate_norm) - detected_len) > max_distance:
            continue
        
        # Calculate distance
        distance = levenshtein_distance(detected_plate, db_plate_norm)
        
        # Check if within tolerance
        if distance <= max_distance:
            # Only calculate ratio if we have a potential match
            ratio = similarity_ratio(detected_plate, db_plate_norm)
            # Prefer closer matches
            if distance < best_distance or (distance == best_distance and ratio > best_ratio):
                best_match = db_data
                best_distance = distance
                best_ratio = ratio
    
    return best_match


def update_session_csv(session_csv_path: str, plate_data: dict):
    """Update session CSV with detected plate data."""
    os.makedirs(os.path.dirname(session_csv_path), exist_ok=True)
    
    file_exists = os.path.exists(session_csv_path)
    
    try:
        with open(session_csv_path, 'a', newline='', encoding='utf-8') as f:
            fieldnames = ['id', 'permanent_parking_id', 'vehicle_number', 'entry_time', 'exit_time', 
                         'duration_minutes', 'created_at', 'updated_at']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            # Generate a simple ID (in production, use proper UUID)
            import uuid
            row = {
                'id': str(uuid.uuid4()),
                'permanent_parking_id': plate_data.get('permanent_parking_id', ''),
                'vehicle_number': plate_data.get('vehicle_number', ''),
                'entry_time': plate_data.get('entry_time', ''),
                'exit_time': plate_data.get('exit_time', ''),
                'duration_minutes': plate_data.get('duration_minutes', ''),
                'created_at': plate_data.get('created_at', ''),
                'updated_at': plate_data.get('updated_at', ''),
            }
            writer.writerow(row)
    except Exception as e:
        print(f"Error updating session CSV: {e}")


