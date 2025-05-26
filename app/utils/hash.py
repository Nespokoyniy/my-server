import bcrypt

def hash_pwd(pwd):
    salt = bcrypt.gensalt()
    bytes = pwd.encode("utf-8")
    hashed_pwd = bcrypt.hashpw(bytes, salt)
    
    return hashed_pwd

def check_pwd(pwd, hashed_pwd):
    bytes = pwd.encode("utf-8")
    return bcrypt.checkpw(bytes, hashed_pwd)