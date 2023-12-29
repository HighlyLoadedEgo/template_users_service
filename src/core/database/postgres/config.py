from pydantic import (
    BaseModel,
    Field,
)


class DatabaseConfig(BaseModel):
    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    password: str = Field(default="PASSWORD")
    user: str = Field(default="USER")
    dbname: str = Field(default="DBNAME")

    def db_url(self, async_: bool = True) -> str:
        if async_:
            return (
                f"postgresql+asyncpg://{self.user}:{self.password}"
                f"@{self.host}:{self.port}/{self.dbname}"
            )
        return (
            f"postgresql://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.dbname}"
        )
