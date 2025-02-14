import bcrypt


def get_password_hash(password: str) -> str:
    """Hash password using bcrypt directly"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash using bcrypt directly"""
    return bcrypt.checkpw(
        password.encode('utf-8'),
        password_hash.encode('utf-8')
    )


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validates that a password meets the minimum requirements:
    - At least 8 characters long
    - Contains both letters and numbers

    Returns:
    - tuple(is_valid: bool, error_message: str)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        return False, "Password must contain both letters and numbers."
    return True, ""
