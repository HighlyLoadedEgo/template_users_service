import bcrypt


def generate_password_hash(password: str) -> str:
    """Generate hashed password."""
    salt = bcrypt.gensalt()
    password_bytes = password.encode("utf-8")
    hash_password = bcrypt.hashpw(password=password_bytes, salt=salt)

    return hash_password.decode("utf-8")


def verify_password_hash(password: str, hashed_password: str) -> bool:
    """Verify hashed password."""
    password_bytes = password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_password_bytes)
