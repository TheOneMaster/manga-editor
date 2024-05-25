import string
import random

characters = string.ascii_letters + string.digits

def randomFilename(size: int = 6):
    return "".join(random.choices(characters, k=size))
