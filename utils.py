import re
import datetime
import cv2


def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append('Minimum 8 characters')
    if not re.search(r'[A-Z]', password):
        errors.append('Uppercase letter (A-Z)')
    if not re.search(r'[a-z]', password):
        errors.append('Lowercase letter (a-z)')
    if not re.search(r'\d', password):
        errors.append('Digit (0-9)')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append('Special character (!@#$%^&*)')
    return errors


def get_password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'[a-z]', password):
        score += 1
    if re.search(r'\d', password):
        score += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    if score <= 2:
        return 'weak', '#f85149'
    elif score <= 4:
        return 'medium', '#d29922'
    else:
        return 'strong', '#238636'


def get_available_cameras():
    cams = []
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cams.append(i)
        cap.release()
    return cams if cams else [0]


def format_time(seconds):
    if seconds is None:
        return '00:00'
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f'{hours:02d}:{minutes:02d}:{secs:02d}'
    return f'{minutes:02d}:{secs:02d}'


def safe_format(value, default=0.0, fmt='.2f'):
    if value is None:
        return format(default, fmt)
    return format(float(value), fmt)


def safe_get(obj, key, default=None):
    return obj.get(key, default) if obj else default


def parse_time_to_minutes(time_str):
    if not time_str or ':' not in time_str:
        return 0
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1]) if len(parts) > 1 else 0
    return hours * 60 + minutes


def validate_time_interval(start_time, end_time):
    start_mins = parse_time_to_minutes(start_time)
    end_mins = parse_time_to_minutes(end_time)
    if end_mins < start_mins:
        end_mins += 24 * 60
    duration = end_mins - start_mins
    if duration <= 0:
        return False, 'End time must be after start time'
    if duration > 1440:
        return False, 'Duration cannot exceed 24 hours'
    if duration < 5:
        return False, 'Minimum duration is 5 minutes'
    return True, f'{duration} minutes'


def get_current_time_minutes():
    now = datetime.datetime.now()
    return now.hour * 60 + now.minute


def is_time_in_range(current_mins, start_time, end_time):
    start_mins = parse_time_to_minutes(start_time)
    end_mins = parse_time_to_minutes(end_time)
    if end_mins < start_mins:
        end_mins += 24 * 60
    return start_mins <= current_mins <= end_mins


def get_session_id():
    return f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"