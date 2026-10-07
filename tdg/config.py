"""
TDG Configuration

------

Pydantic Settings reads every value from your .env file and validates them.
If a required value is missing or the wrong type, it fails loduly on startup rather than crashing mysteriously later during a request

Usage anwhere in the app:
    from tdg.confg import settings
    print(settings.postgres_host)
"""

from functools import lru_cache
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    All Application configurations live here.
    Pydantic reads each field from environment variables ( or .env file).
    Field names map to env var names - postgres_host reads POSTGRES_HOST.
    Types are validated automatically - If PORT is "abc", it fails on startup.
    """

    # - Tell Pydantic where to find the .env file ---
    model_config = SettingsConfigDict(
        env_file = ".env",  # Load from .env in project root
        env_file_encoding = "utf-8",
        case_sensitive = False, # POSTGRES_HOST and postgres_host both work
        extra="ignore", # ignore any extra vars in .env we don't use
    )

    # -- Application ---
    app_name: str = Field(default="test-data-generator")
    app_env: str = Field(default="development")
    app_port: int = Field(default=8000)
    log_level: str = Field(default="INFO")

    # -- PostgreSQL----
    # Each part read separately so we can build the URL programmatically
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_db: str = Field(default="postgres")
    postgres_user: str = Field(default="tdg_user")
    postgres_password: str = Field(default="tdgpassword")

    # -- Redis ---
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_db: int = Field(default=0)

    # -- Generation Settings --
    default_profile: str = Field(default="residential_smart")
    max_records_per_run: int = Field(default=10000)
    max_retries_per_entity: int = Field(default=3)
    generation_timeout_seconds: int = Field(default=300)

    # -- Export ---
    export_dir: str = Field(default="./export")
    export_max_file_size_mb: int = Field(default=100)

    # -- Observability ---
    prometheus_port: int = Field(default=9090)
    enable_metrics: bool = Field(default=True)

    # -- Computed Fields --
    # these are built automtically from the indiividual fields above.
    # Never set these in .env - Pydantic calculates them. 

    @computed_field
    @property
    def database_url(self) -> str:
        """Asycnc database URL for SQLAlchemy.
        Uses psycog(v3) driver - note 'postgresql+psycopg' not 'pyscopg2'.
        This is what SQLAlchey uses for all async DB operations.
        """
        return (
            f"postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"{self.postgres_db}"
        )

    @computed_field
    @property
    def database_url_sync(self) -> str:
        """
        Sync Database URL for Alembic migrations.
        Alembic does not support async so it needs the sync driver.
        Same connection details, different driver prefix.
        """

        return (
            f"postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"{self.postgres_db}"
        )

    @computed_field
    @property
    def redis_url(self) -> str:
        """ Redis connection URL for Celery broker and result backend.
        format: redis://host:port/db_number"""
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @computed_field
    @property
    def is_development(self) -> bool:
        """Convenience flag - True when running locally."""
        return self.app_env== "development"

    @computed_field
    @property
    def is_production(self) -> bool:
        """Convenience flag - True when running in production."""
        return self.app_env== "production"

    @lru_cache
    def get_settings() -> "Settings":
        """
        Returns the settings singleton.

        @lru-cache means this function only runs ONCE - the first time it's called.
        Every Subsequent call returns the same cahced Settings object.
        This Means. env is only read once at startup, not every request.

        Usage:
            from tdg.config import settings  <- use this everyhere
            settings = get_settings() <- same thing
        """
        return Settings()


    # Module-level singleton - import this directly
    # from tdg.config import settings
    settings: Settings = get_settings()
    


    
