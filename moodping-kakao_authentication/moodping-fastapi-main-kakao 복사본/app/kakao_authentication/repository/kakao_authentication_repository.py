from __future__ import annotations

from abc import ABC, abstractmethod

from app.kakao_authentication.service.schemas import KakaoLoginResult, KakaoUserInfo


class KakaoAuthenticationRepository(ABC):
    @abstractmethod
    async def fetch_access_token(self, code: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def fetch_user_info(self, access_token: str) -> KakaoUserInfo:
        raise NotImplementedError

    async def login(self, code: str) -> KakaoLoginResult:
        access_token = await self.fetch_access_token(code)
        user_info = await self.fetch_user_info(access_token)
        return KakaoLoginResult(access_token=access_token, user_info=user_info)

