import random

def otp_generator(length = 6):
    otp = ''
    for _ in range(length):
        otp += str(random.randint(0,9))
    
    return otp