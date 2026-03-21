import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from backend.main import login_user
from backend import models

def test_login_success_unit():
    """Doğru email ve şifre ile giriş yapılabiliyor mu kontrol edilir."""
    # Veritabanı taklidi
    mock_db = MagicMock()
    
    # Test verisi, veritabanında bulunan
    mock_user = models.User(
        userID=1,
        fullName="Test Kullanici",
        email="test@vita.com",
        passwordHash="fake_hash_value"
    )
    # Veritabanı sorgusu sonucu kullanıcı dönmeli
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    # Şifre doğrulama ve token üretme
    # Şifre doğrulaması 'True' dönsün ve sabit bir token üretilsin
    with patch("backend.auth.verify_password", return_value=True), \
         patch("backend.auth.create_access_token", return_value="test_token_123"):
        
        # Kullanıcı tarafından alınan bilgiler
        login_data = {"email": "test@vita.com", "password": "dogru_sifre"}
        # login fonksiyonu
        result = login_user(login_data=login_data, db=mock_db)

        # Doğrulama , sonuçların kontrol edilmesi
        assert result["access_token"] == "test_token_123"
        assert result["token_type"] == "bearer"
        assert "Hos geldin Test Kullanici" in result["mesaj"]

def test_login_wrong_password_unit():
    """Kullanıcı var ama şifre yanlışsa hata dönüyor mu kontrol edilir."""
    mock_db = MagicMock()
    
    # Kullanıcı veritabanında var
    mock_user = models.User(email="test@vita.com", passwordHash="hash")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    # Şifre doğrulaması 'False' dönsün 
    with patch("backend.auth.verify_password", return_value=False):
        login_data = {"email": "test@vita.com", "password": "yanlis_sifre"}
        # Hata oluşup oluşmadığı kontrol edilir
        with pytest.raises(HTTPException) as exc_info:
            login_user(login_data=login_data, db=mock_db)
        # Hata içeriği
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "E-posta veya sifre hatali."

def test_login_user_not_found_unit():
    """Eğer kullanıcı veritabanında yoksa hata dönüyor mu kontrol edilir."""
    mock_db = MagicMock()
    
    # Sorgu sonucu 'None' dönsün (Kullanıcı yok)
    mock_db.query.return_value.filter.return_value.first.return_value = None

    login_data = {"email": "olmayan@vita.com", "password": "sifre"}
    
    with pytest.raises(HTTPException) as exc_info:
        login_user(login_data=login_data, db=mock_db)
    
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "E-posta veya sifre hatali."