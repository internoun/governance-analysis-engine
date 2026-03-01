from governance_analysis_engine.config import Settings


def test_default_settings() -> None:
    """Test that settings have correct default values."""
    settings = Settings(_env_file=None)
    assert settings.app_name == "governance-analysis-engine"
    assert settings.log_level == "INFO"


def test_settings_with_env_override() -> None:
    """Test that settings can be overridden via environment variables."""
    settings = Settings(
        _env_file=None,
        app_name="custom-app-name",
        log_level="DEBUG",
    )
    assert settings.app_name == "custom-app-name"
    assert settings.log_level == "DEBUG"


def test_settings_with_env_file_support() -> None:
    """Test that settings support env_file configuration."""
    settings = Settings(_env_file=".env")
    # Should not raise an error even if .env doesn't exist
    assert settings.app_name == "governance-analysis-engine"
