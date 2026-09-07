from argon2 import PasswordHasher



ph = PasswordHasher()

def hash_passw(password):
    hashed_password = ph.hash(password)
    
    return hashed_password



def compare_passwords(returned_hashed, password):

    compared = ph.verify(returned_hashed, password)

    return compared
