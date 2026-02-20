from __future__ import annotations

from abc import ABC, abstractmethod

from app.kakao_authentication.service.schemas import KakaoLoginResult


class KakaoAuthenticationService(ABC):
    @abstractmethod
    def generate_oauth_url(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def login_with_kakao(self, code: str) -> KakaoLoginResult:
        raise NotImplementedError

