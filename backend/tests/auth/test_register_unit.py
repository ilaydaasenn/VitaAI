import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from backend.main import register_user

def test_register_success_unit():
    """Kullanıcı kaydı başarılı olduğunda fonksiyon doğru çalışıyor mu test edilir."""
    # Veritabanı taklidi
    mock_db = MagicMock()
    
    # Kullanıcı yok
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Test Verisi
    test_payload = {
        "full_name": "Unit Test Kullanici",
        "email": "unit@test.com",
        "password": "sifre_test_123"
    }

    # Test edilecek fonksiyon
    result = register_user(user_data=test_payload, db=mock_db)

    # Doğrulama
    assert result["mesaj"] == "Kayit basarili!"
    assert "userID" in result
    
    # DB fonksiyonlarının çağrıldığını doğrulama
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    # Veritabanına kaydedilecek son kullanıcı verisi
    added_user = mock_db.add.call_args[0][0]

    # Şifre güvenliği kontrolü
    # hashlenerek(şifrelenerek) saklama
    assert added_user.passwordHash != "sifre_test_123"
    assert len(added_user.passwordHash) > 30
    
    # Veri tutarlılığı, gelen veriler doğru şekilde eklenmesi kontrolü
    assert added_user.fullName == "Unit Test Kullanici"
    assert added_user.email == "unit@test.com"

def test_register_duplicate_email_unit():
    """Aynı e-posta varsa hata veriyor mu kontrol edilir."""
    mock_db = MagicMock()
    
    # Kullanıcı var
    mock_db.query.return_value.filter.return_value.first.return_value = MagicMock()

    test_payload = {
        "full_name": "Unit Test",
        "email": "unit@test.com",
        "password": "sifre"
    }

    # HTTPException(400)
    with pytest.raises(HTTPException) as exc_info:
        register_user(user_data=test_payload, db=mock_db)

    # Hata içeriği kontrolü
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Bu e-posta zaten kayitli."