from src.services.encrypt_service import EncryptService


class TestEncryptServiceCreation:
    def test_create_encrypt_service(self) -> None:
        service = EncryptService("mypassword")

        assert service is not None

    def test_password_property_returns_original(self) -> None:
        service = EncryptService("mypassword")

        assert service.password == "mypassword"

    def test_password_is_stored_correctly(self) -> None:
        password = "testpassword123"
        service = EncryptService(password)

        assert service.password == password


class TestEncryptServicePasswordHashed:
    def test_password_hashed_returns_string(self) -> None:
        service = EncryptService("mypassword")

        result = service.password_hashed

        assert isinstance(result, str)

    def test_password_hashed_is_not_original(self) -> None:
        password = "mypassword"
        service = EncryptService(password)

        result = service.password_hashed

        assert result != password

    def test_password_hashed_is_not_empty(self) -> None:
        service = EncryptService("mypassword")

        result = service.password_hashed

        assert len(result) > 0

    def test_password_hashed_generates_different_hashes(self) -> None:
        service = EncryptService("mypassword")

        hash1 = service.password_hashed
        hash2 = service.password_hashed

        assert hash1 != hash2

    def test_password_hashed_contains_algorithm_info(self) -> None:
        service = EncryptService("mypassword")

        result = service.password_hashed

        assert "scrypt" in result or "pbkdf2" in result or "$" in result


class TestEncryptServiceValidPassword:
    def test_valid_password_returns_true_for_correct_password(self) -> None:
        password = "mypassword"
        service = EncryptService(password)
        hashed = service.password_hashed

        result = service.valid_password(hashed)

        assert result is True

    def test_valid_password_returns_false_for_wrong_password(self) -> None:
        service1 = EncryptService("correctpassword")
        hashed = service1.password_hashed

        service2 = EncryptService("wrongpassword")
        result = service2.valid_password(hashed)

        assert result is False

    def test_valid_password_is_case_sensitive(self) -> None:
        service1 = EncryptService("MyPassword")
        hashed = service1.password_hashed

        service2 = EncryptService("mypassword")
        result = service2.valid_password(hashed)

        assert result is False

    def test_valid_password_works_with_special_characters(self) -> None:
        password = "p@$$w0rd!#%&"
        service = EncryptService(password)
        hashed = service.password_hashed

        result = service.valid_password(hashed)

        assert result is True

    def test_valid_password_works_with_unicode(self) -> None:
        password = "contraseña123"
        service = EncryptService(password)
        hashed = service.password_hashed

        result = service.valid_password(hashed)

        assert result is True

    def test_valid_password_works_with_long_password(self) -> None:
        password = "a" * 100
        service = EncryptService(password)
        hashed = service.password_hashed

        result = service.valid_password(hashed)

        assert result is True

    def test_valid_password_works_with_short_password(self) -> None:
        password = "a"
        service = EncryptService(password)
        hashed = service.password_hashed

        result = service.valid_password(hashed)

        assert result is True


class TestEncryptServiceEdgeCases:
    def test_empty_password(self) -> None:
        service = EncryptService("")
        hashed = service.password_hashed

        result = service.valid_password(hashed)

        assert result is True

    def test_whitespace_password(self) -> None:
        service = EncryptService("   ")
        hashed = service.password_hashed

        result = service.valid_password(hashed)

        assert result is True

    def test_password_with_newlines(self) -> None:
        password = "pass\nword"
        service = EncryptService(password)
        hashed = service.password_hashed

        result = service.valid_password(hashed)

        assert result is True

    def test_password_with_tabs(self) -> None:
        password = "pass\tword"
        service = EncryptService(password)
        hashed = service.password_hashed

        result = service.valid_password(hashed)

        assert result is True
