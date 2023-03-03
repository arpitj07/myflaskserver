import bcrypt
from random import randint, randrange

# Takes password as parameter and return encrypted password
def encryptPass(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)
   
# Takes password as parameter and return decrypted password
def decryptPass(password, hash):
    return bcrypt.checkpw(password.encode('utf-8'), hash)

# function to generate random number
def genID(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)