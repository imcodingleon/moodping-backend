from __future__ import annotations

from urllib.parse import urlencode

from fastapi import HTTPException

from app.kakao_authentication.config.kakao_config import KakaoConfig
from app.kakao_authentication.repository.kakao_authentication_repository_impl import (
    KakaoAuthenticationRepositoryImpl,
)
from app.kakao_authentication.service.kakao_authentication_service import (
    KakaoAuthenticationService,
)
from app.kakao_authentication.service.schemas import KakaoLoginResult


class KakaoAuthenticationServiceImpl(KakaoAuthenticationService):
    _instance: "KakaoAuthenticationServiceImpl | None" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._repo = KakaoAuthenticationRepositoryImpl.get_instance()
        return cls._instance

    @classmethod
    def get_instance(cls) -> "KakaoAuthenticationServiceImpl":
        return cls()

    def generate_oauth_url(self) -> str:
        client_id = KakaoConfig.client_id()
        redirect_uri = KakaoConfig.redirect_uri()
        if not client_id or not redirect_uri:
            raise HTTPException(status_code=500, detail="카카오 OAuth 설정이 누락되었습니다.")

        params = urlencode(
            {
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "response_type": "code",
            }
        )
        return f"{KakaoConfig.auth_base_url}?{params}"

    async def login_with_kakao(self, code: str) -> KakaoLoginResult:
        return await self._repo.login(code)

