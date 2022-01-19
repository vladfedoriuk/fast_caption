from .base import Settings as MyBaseSettings


class Settings(MyBaseSettings):
    test_postgres_db: str = "caption-test"

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.test_postgres_db}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
