from passlib.context import CryptContext
from .common_utility import config

SECRET_KEY = config["jwt"]["secret"]
ALGORITHM = config["jwt"]["algorithm"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

