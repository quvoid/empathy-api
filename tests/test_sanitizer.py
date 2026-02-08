import pytest
from src.core.sanitizer import Sanitizer


class TestSanitizer:
    """Test suite for the Sanitizer class."""

    def test_sanitize_email(self):
        """Should redact email addresses."""
        text = "Error for user john.doe@example.com"
        result = Sanitizer.sanitize(text)
        assert "[EMAIL_REDACTED]" in result
        assert "john.doe@example.com" not in result

    def test_sanitize_ip_address(self):
        """Should redact IP addresses."""
        text = "Connection failed from 192.168.1.100"
        result = Sanitizer.sanitize(text)
        assert "[IP_REDACTED]" in result
        assert "192.168.1.100" not in result

    def test_sanitize_jwt_token(self):
        """Should redact JWT tokens."""
        jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
        text = f"Auth failed with token {jwt}"
        result = Sanitizer.sanitize(text)
        assert "[TOKEN_REDACTED]" in result
        assert jwt not in result

    def test_sanitize_api_key(self):
        """Should redact API keys."""
        text = "api_key=sk_test_12345678"
        result = Sanitizer.sanitize(text)
        assert "[SECRET_REDACTED]" in result
        assert "sk_test_12345678" not in result

    def test_sanitize_uuid(self):
        """Should redact UUIDs."""
        text = "User 550e8400-e29b-41d4-a716-446655440000 not found"
        result = Sanitizer.sanitize(text)
        assert "[ID_REDACTED]" in result
        assert "550e8400-e29b-41d4-a716-446655440000" not in result

    def test_sanitize_file_path_windows(self):
        """Should redact Windows file paths."""
        text = r"Error reading C:\Users\admin\secrets\passwords.txt"
        result = Sanitizer.sanitize(text)
        assert "[PATH_REDACTED]" in result

    def test_sanitize_file_path_unix(self):
        """Should redact Unix file paths."""
        text = "Error reading /home/user/.ssh/id_rsa"
        result = Sanitizer.sanitize(text)
        assert "[PATH_REDACTED]" in result

    def test_sanitize_empty_string(self):
        """Should handle empty strings gracefully."""
        assert Sanitizer.sanitize("") == ""
        assert Sanitizer.sanitize(None) == ""

    def test_sanitize_no_sensitive_data(self):
        """Should not modify text without sensitive data."""
        text = "ZeroDivisionError: division by zero"
        result = Sanitizer.sanitize(text)
        assert result == text

    def test_sanitize_multiple_sensitive_items(self):
        """Should handle multiple sensitive items in one string."""
        text = "User john@test.com at 10.0.0.1 had error"
        result = Sanitizer.sanitize(text)
        assert "[EMAIL_REDACTED]" in result
        assert "[IP_REDACTED]" in result
        assert "john@test.com" not in result
        assert "10.0.0.1" not in result
