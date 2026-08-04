from fastapi.security import HTTPBearer
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    fake_access_token: str = "secret-token-123"

    mysql_host: str = "db"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = "my-secret-pw"
    mysql_database: str = "mydb"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )


settings = Settings()
FAKE_ACCESS_TOKEN = settings.fake_access_token

# 只用來讓 Swagger UI 顯示 Authorize 鎖頭並在 OpenAPI schema 標記需要 token，
# 實際驗證交給 main.py 的 verify_token_middleware，故 auto_error=False。
security = HTTPBearer(auto_error=False)
