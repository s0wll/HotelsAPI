from pydantic_settings import BaseSettings, SettingsConfigDict

'''Класс Settings наследует от BaseSettings и используется для управления конфигурацией приложения'''
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # DSN - стандартный синтаксис адреса для подключения к базе данных
    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env")  # Конфигурация модели, указывающая на файл окружения


settings = Settings()  # Создание экземпляра класса Settings для доступа к настройкам
