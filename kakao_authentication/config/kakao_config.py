import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class KakaoConfig(BaseSettings):
    KAKAO_AUTH_URL: str = "https://kauth.kakao.com/oauth/authorize"
    KAKAO_TOKEN_URL: str = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL: str = "https://kapi.kakao.com/v2/user/me"
    
    # settings.py의 값을 그대로 가져오거나, 환경변수에서 읽어옵니다.
    # 여기서는 환경변수 의존성을 유지하도록 설정
    kakao_client_id: str = ""
    kakao_client_secret: str = ""
    kakao_redirect_uri: str = "http://localhost:33333/kakao-authentication/request-access-token-after-redirection"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache
def get_kakao_config() -> KakaoConfig:
    return KakaoConfig()
