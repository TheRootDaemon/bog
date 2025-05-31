from datetime import datetime, timedelta
from jose import JWTError, jwt

secretKey = "I love salted peanuts very much"
algorithm = "HS256"
expiration = 60


def generateToken(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=expiration))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secretKey, algorithm=algorithm)
    return encoded_jwt
