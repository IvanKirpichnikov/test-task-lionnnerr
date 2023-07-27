from random import SystemRandom
from string import ascii_letters


def random_key() -> str:
    symbols = SystemRandom().sample(ascii_letters, 2)
    key = ''.join(symbols)
    
    return key
