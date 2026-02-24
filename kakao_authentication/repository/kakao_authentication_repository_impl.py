import logging
import httpx
from typing import Dict, Any

from moodping.kakao_authentication.repository.kakao_authentication_repository import KakaoAuthenticationRepository
from moodping.kakao_authentication.config.kakao_config import get_kakao_config

logger = logging.getLogger(__name__)

class KakaoAuthenticationRepositoryImpl(KakaoAuthenticationRepository):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KakaoAuthenticationRepositoryImpl, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.config = get_kakao_config()
            self.initialized = True

    async def fetch_access_token(self, code: str) -> str | None:
        data = {
            "grant_type": "authorization_code",
            "client_id": self.config.kakao_client_id,
            "redirect_uri": self.config.kakao_redirect_uri,
            "code": code,
        }
        if self.config.kakao_client_secret:
            data["client_secret"] = self.config.kakao_client_secret

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self.config.KAKAO_TOKEN_URL,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"},
            )
        
        if resp.status_code != 200:
            logger.error("카카오 토큰 요청 실패: %s %s", resp.status_code, resp.text)
            return None
            
        return resp.json().get("access_token")

    async def fetch_user_info(self, access_token: str) -> Dict[str, Any] | None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                self.config.KAKAO_USER_INFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            
        if resp.status_code != 200:
            logger.error("카카오 유저 정보 요청 실패: %s %s", resp.status_code, resp.text)
            return None

        data = resp.json()
        kakao_id = str(data["id"])
        properties = data.get("properties", {})
        
        return {
            "kakao_id": kakao_id,
            "nickname": properties.get("nickname"),
            "profile_image": properties.get("profile_image"),
        }
