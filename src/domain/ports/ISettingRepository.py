# Aplicación
from abc import ABC, abstractmethod


class ISettingRepository(ABC):
    @abstractmethod
    def get_secret_key(self) -> str:
        pass

    @abstractmethod
    def get_encryption_algorithm(self) -> str:
        pass

    @abstractmethod
    def get_access_token_expire_minutes(self) -> int:
        pass

    @abstractmethod
    def get_refresh_token_expire_days(self) -> int:
        pass
