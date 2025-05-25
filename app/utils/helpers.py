from datetime import datetime
from typing import Optional

def format_date(date_obj) -> str:
    """Format date object to readable string"""
    if date_obj:
        return date_obj.strftime("%Y-%m-%d")
    return ""

def format_datetime(datetime_obj) -> str:
    """Format datetime object to readable string"""
    if datetime_obj:
        return datetime_obj.strftime("%Y-%m-%d %H:%M")
    return ""

def calculate_letter_grade(numeric_grade: float) -> str:
    """Convert numeric grade to letter grade"""
    if numeric_grade >= 90:
        return "A"
    elif numeric_grade >= 80:
        return "B"
    elif numeric_grade >= 70:
        return "C"
    elif numeric_grade >= 60:
        return "D"
    else:
        return "F"

def is_passing_grade(grade: float) -> bool:
    """Check if grade is passing (>= 60)"""
    return grade >= 60.0 if grade is not None else False

def validate_username(username: str) -> bool:
    """Validate username format"""
    return len(username) >= 3 and username.isalnum()

def validate_password(password: str) -> bool:
    """Basic password validation"""
    return len(password) >= 6