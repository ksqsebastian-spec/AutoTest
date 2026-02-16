"""Tests for German validators."""

from app.utils.validators import validate_iban_de, validate_plz, validate_ust_id


class TestValidateUstId:
    def test_valid(self):
        assert validate_ust_id("DE123456789") is True

    def test_valid_with_spaces(self):
        assert validate_ust_id("DE 123456789") is True

    def test_invalid_prefix(self):
        assert validate_ust_id("AT123456789") is False

    def test_too_short(self):
        assert validate_ust_id("DE12345") is False


class TestValidateIBAN:
    def test_valid(self):
        assert validate_iban_de("DE89370400440532013000") is True

    def test_valid_with_spaces(self):
        assert validate_iban_de("DE89 3704 0044 0532 0130 00") is True

    def test_invalid(self):
        assert validate_iban_de("GB82WEST12345698765432") is False


class TestValidatePLZ:
    def test_valid(self):
        assert validate_plz("10115") is True

    def test_invalid(self):
        assert validate_plz("1011") is False

    def test_with_whitespace(self):
        assert validate_plz(" 10115 ") is True
