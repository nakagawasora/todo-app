def isValidTitle(title: str) -> bool:
    trimmed = title.strip()
    if len(trimmed) == 0:
        return False
    if len(trimmed) > 100:
        return False
    return True
