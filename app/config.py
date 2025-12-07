"""Configuration management using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str
    
    # Weekly Picks Configuration
    espn_game_data_link: str = "https://www.espn.com/nfl/schedule/_/week/13/year/2025/seasontype/2"
    slate_description: str = "Sunday main slate"
    note: str = "All players checked against latest depth charts, injury reports, and preview/fantasy articles."
    
    # Game Focus
    focus_games: str = "all"  # "all", "afternoon_only", "early_only", "primetime_only", or comma-separated list
    
    # Prop Focus
    prop_focus: str = "mix"  # "overs", "unders", or "mix"
    
    # AI Generation Settings
    min_articles_for_sentiment: int = 3
    include_long_shots: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Allow extra fields in .env file
    )


# Global settings instance
settings = Settings()