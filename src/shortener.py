import string
from secrets import choice


ALPHABET: str = string.ascii_letters + string.digits

def generate_random_string(length: int = 6) -> str:
    return ''.join(choice(ALPHABET) for _ in range(length))
