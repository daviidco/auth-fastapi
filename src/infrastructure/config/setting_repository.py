from src.domain.ports.ISettingRepository import ISettingRepository
from src.infrastructure.config.settings import Settings


class SettingRepository(ISettingRepository):
    def __init__(self, settings: Settings):
        self.settings = settings

    def get_secret_key(self) -> str:
        return self.settings.SECRET_KEY

    def get_encryption_algorithm(self) -> str:
        return self.settings.ALGORITHM

    def get_access_token_expire_minutes(self) -> int:
        return self.settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def get_refresh_token_expire_days(self) -> int:
        return self.settings.REFRESH_TOKEN_EXPIRE_DAYS
