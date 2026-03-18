from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Docker üzerinde çalışan veritabanına bağlanmak için gerekli adres bilgileri.
SQLALCHEMY_DATABASE_URL = "postgresql://vitaai_admin:VitaAI_20262808@localhost:5432/vitaai_db"

# Veritabanı ile Python arasındaki iletişimi sağlayan ana bağlantı.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Veritabanı işlemleri için kullanılacak oturumları(session) yöneten yapı.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Veritabanındaki tabloları Python sınıfları olarak tanımlarken kullanılacak ana sınıf.
Base = declarative_base()

# Veritabanı bağlantısını açıp işlem bitince kapatan fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()