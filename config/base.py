from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = "caption"
    postgres_password: str = "caption"
    postgres_host: str = "127.0.0.1"
    postgres_port: str = "15432"
    postgres_db: str = "caption"

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
