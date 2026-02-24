from abc import ABC, abstractmethod
from typing import Dict, Any

class KakaoAuthenticationService(ABC):
    @abstractmethod
    def generate_oauth_url(self) -> str:
        pass

    @abstractmethod
    async def login_with_kakao(self, code: str) -> Dict[str, Any]:
        """
        code를 받아 카카오 엑세스 토큰을 발급받고, 유저 정보를 조회하여 반환합니다.
        """
        pass
