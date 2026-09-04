class TokenAnalyzerError(Exception):
    """Base exception for the token analyzer system."""
    pass


class ProviderError(TokenAnalyzerError):
    """Raised when a provider fails to fetch or parse data."""
    def __init__(self, provider: str, message: str):
        super().__init__(f"[{provider}] {message}")


class SecurityViolation(TokenAnalyzerError):
    """Raised when a hard security rule is violated."""
    def __init__(self, reason: str):
        super().__init__(f"Security violation: {reason}")


class InvalidRegistry(TokenAnalyzerError):
    """Raised when registry or schema is invalid."""
    def __init__(self, message: str):
        super().__init__(f"Registry error: {message}")


if __name__ == "__main__":
    print("exceptions ready.")
