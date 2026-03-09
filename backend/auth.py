from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

#Şifreleme Ayarları
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


SECRET_KEY = "VITAAI_GIZLI_ANAHTAR"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120 

#Şifre Doğrulaması
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#Başarılı giriş sonucu , giriş kartı
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt