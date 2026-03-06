from fastapi import FastAPI

# Uygulama başlangıcı
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