def key_loader(path: str) -> str:
    """Load key from file."""
    with open(path, "rb") as file:
        key = file.read()

    return key.decode("utf-8")
