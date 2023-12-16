import bcrypt


def generate_password_hash(password: str) -> bytes:
    """Generate hashed password."""
    salt = bcrypt.gensalt()
    password_bytes = password.encode("utf-8")
    hash_password = bcrypt.hashpw(password=password_bytes, salt=salt)

    return hash_password


def verify_password_hash(password: str, hashed_password: bytes) -> bool:
    """Verify hashed password."""
    password_bytes = password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_password)
