from src.models.Encrypt import Encrypt

from test.constants import HASH_PASSWORD


def test_init_encrypt(encrypt_model: Encrypt) -> None:
    assert encrypt_model
    assert encrypt_model.password
    assert encrypt_model.password_hashed
    assert isinstance(encrypt_model.password, str)
    assert isinstance(encrypt_model.password_hashed, str)

def test_valid_password_encrypt(encrypt_model: Encrypt) -> None:
    assert encrypt_model.valid_password(pwhash=HASH_PASSWORD)

def test_not_valid_password_encrypt(encrypt_model: Encrypt) -> None:
    assert not encrypt_model.valid_password(pwhash="pepe")