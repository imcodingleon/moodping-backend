from dataclasses import dataclass

from app.config import get_settings


@dataclass(frozen=True)
class KakaoConfig:
    auth_base_url: str = "https://kauth.kakao.com/oauth/authorize"
    token_url: str = "https://kauth.kakao.com/oauth/token"
    user_info_url: str = "https://kapi.kakao.com/v2/user/me"

    @staticmethod
    def client_id() -> str:
        return get_settings().kakao_client_id

    @staticmethod
    def client_secret() -> str:
        return get_settings().kakao_client_secret

    @staticmethod
    def redirect_uri() -> str:
        return get_settings().kakao_redirect_uri

