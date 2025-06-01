from passlib.context import CryptContext

def verify_password(plain_password, hashed_password):
 
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(plain_password, hashed_password)