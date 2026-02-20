from __future__ import annotations

import logging

import httpx
from fastapi import HTTPException

from app.kakao_authentication.config.kakao_config import KakaoConfig
from app.kakao_authentication.repository.kakao_authentication_repository import (
    KakaoAuthenticationRepository,
)
from app.kakao_authentication.service.schemas import KakaoUserInfo

logger = logging.getLogger(__name__)


class KakaoAuthenticationRepositoryImpl(KakaoAuthenticationRepository):
    _instance: "KakaoAuthenticationRepositoryImpl | None" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> "KakaoAuthenticationRepositoryImpl":
        return cls()

    async def fetch_access_token(self, code: str) -> str:
        if not code:
            raise HTTPException(status_code=400, detail="인가 코드가 필요합니다.")

        client_id = KakaoConfig.client_id()
        redirect_uri = KakaoConfig.redirect_uri()
        if not client_id or not redirect_uri:
            raise HTTPException(status_code=500, detail="카카오 OAuth 설정이 누락되었습니다.")

        data: dict[str, str] = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code,
        }
        client_secret = KakaoConfig.client_secret()
        if client_secret:
            data["client_secret"] = client_secret

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    KakaoConfig.token_url,
                    data=data,
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
                    },
                )
        except httpx.RequestError as e:
            logger.exception("Kakao token request failed: %s", e)
            raise HTTPException(status_code=502, detail="Kakao 서버 요청 실패") from e

        if resp.status_code != 200:
            logger.error("Kakao token error: %s %s", resp.status_code, resp.text)
            raise HTTPException(
                status_code=400,
                detail=f"Kakao 토큰 요청 실패: {resp.text}",
            )

        access_token = resp.json().get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="Kakao access_token이 없습니다.")
        return str(access_token)

    async def fetch_user_info(self, access_token: str) -> KakaoUserInfo:
        if not access_token:
            raise HTTPException(status_code=401, detail="액세스 토큰이 필요합니다.")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    KakaoConfig.user_info_url,
                    headers={"Authorization": f"Bearer {access_token}"},
                )
        except httpx.RequestError as e:
            logger.exception("Kakao userinfo request failed: %s", e)
            raise HTTPException(status_code=502, detail="Kakao 사용자 정보 요청 실패") from e

        if resp.status_code != 200:
            logger.error("Kakao userinfo error: %s %s", resp.status_code, resp.text)
            raise HTTPException(
                status_code=401,
                detail="유효하지 않거나 만료된 액세스 토큰입니다.",
            )

        data = resp.json()
        kakao_id = str(data.get("id", ""))
        if not kakao_id:
            raise HTTPException(status_code=400, detail="Kakao 사용자 id가 없습니다.")

        properties = data.get("properties") or {}
        return KakaoUserInfo(
            kakao_id=kakao_id,
            nickname=properties.get("nickname"),
            profile_image=properties.get("profile_image"),
        )

