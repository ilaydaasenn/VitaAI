from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db 
from backend import models, auth

app = FastAPI(title="VitaAI API Servisi")

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
    hashed_pw = auth.pwd_context.hash(user_data.get("password"))

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

@app.post("/login")
def login_user(login_data: dict, db: Session = Depends(get_db)):
    # e-posta ile kullanıcı kontrolü
    user = db.query(models.User).filter(models.User.email == login_data.get("email")).first()
    
    # Kullanıcı yoksa veya şifre yanlışsa
    if not user or not auth.verify_password(login_data.get("password"), user.passwordHash):
        raise HTTPException(status_code=401, detail="E-posta veya sifre hatali.")

    # başarılı giriş sonucu , giriş kartı
    access_token = auth.create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "mesaj": f"Hos geldin {user.fullName}!"
    }