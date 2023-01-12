import random
from string import digits


def generate_code():
    return ''.join(random.choices(digits, k=4))