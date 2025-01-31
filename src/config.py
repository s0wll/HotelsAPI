from pydantic_settings import BaseSettings, SettingsConfigDict

'''Класс Settings наследует от BaseSettings и используется для управления конфигурацией приложения'''
class Settings(BaseSettings):  
    DB_NAME: str
    model_config = SettingsConfigDict(env_file=".env")  # Конфигурация модели, указывающая на файл окружения


settings = Settings()  # Создание экземпляра класса Settings для доступа к настройкам
