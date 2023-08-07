import random
import string

def generate_referral():
    characters = string.digits + string.ascii_uppercase
    code = ''.join(random.choice(characters) for _ in range(6))
    return code

def generate_code():
    return random.randint(1000, 9999)
