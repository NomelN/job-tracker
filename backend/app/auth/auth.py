from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer

load_dotenv()

# Sécurité
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
EMAIL_TOKEN_SECRET = os.getenv("EMAIL_TOKEN_SECRET")

serializer = URLSafeTimedSerializer(EMAIL_TOKEN_SECRET)
 

# Hash du mot de passe
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def generate_email_token(email: str) -> str:
    return serializer.dumps(email, salt="email-confirm")

def verify_email_token(token: str, max_age: int = 3600) -> str:
    return serializer.loads(token, salt="email-confirm", max_age=max_age)
