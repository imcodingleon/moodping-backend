from abc import ABC, abstractmethod
from typing import Dict, Any

class KakaoAuthenticationRepository(ABC):
    @abstractmethod
    async def fetch_access_token(self, code: str) -> str | None:
        pass

    @abstractmethod
    async def fetch_user_info(self, access_token: str) -> Dict[str, Any] | None:
        pass
