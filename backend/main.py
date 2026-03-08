from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend.database import get_db 
from backend import models

app = FastAPI(title="VitaAI API Servisi")

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@app.get("/")
def ana_sayfa():
    return {
        "durum": "Calisiyor",
        "mesaj": "VitaAI Backend Servisi",
        "versiyon": "1.0.0"
    }

@app.get("/test")
def test_et():
    return {"bilgi": "Bu servis hem mobil hem web icin ortak veri kaynagidir."}

@app.post("/register")
def register_user(user_data: dict, db: Session = Depends(get_db)):
    # E-posta kontrolü
    existing_user = db.query(models.User).filter(models.User.email == user_data.get("email")).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayitli.")

    # Şifreyi hashleyerek güvenli saklama
    hashed_pw = get_password_hash(user_data.get("password"))

    # Yeni kullanıcı oluşturma
    new_user = models.User(
        fullName=user_data.get("full_name"), 
        email=user_data.get("email"),        
        passwordHash=hashed_pw               
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    
    return {"mesaj": "Kayit basarili!", "userID": new_user.userID}