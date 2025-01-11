# File: backend/app/utils/helpers.py

# This file contains helper functions that provide common functionality used throughout the application.

def format_response(data, message="", status_code=200):
    return {
        "status": status_code,
        "message": message,
        "data": data
    }

def validate_input(data, required_fields):
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    return True, "Validation successful"

def log_error(error_message):
    # Placeholder for logging error messages
    print(f"ERROR: {error_message}")