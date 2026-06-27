from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta


SECRET_KEY = "sentinelvault-secret-key"
ALGORITHM = "HS256"


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def create_token(data: dict):

    token_data = data.copy()

    expire = datetime.utcnow() + timedelta(hours=1)

    token_data.update({
        "exp": expire
    })

    token = jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token
