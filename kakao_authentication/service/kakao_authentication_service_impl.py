from urllib.parse import urlencode
from typing import Dict, Any

from moodping.kakao_authentication.service.kakao_authentication_service import KakaoAuthenticationService
from moodping.kakao_authentication.repository.kakao_authentication_repository import KakaoAuthenticationRepository
from moodping.kakao_authentication.config.kakao_config import get_kakao_config

class KakaoAuthenticationServiceImpl(KakaoAuthenticationService):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(KakaoAuthenticationServiceImpl, cls).__new__(cls)
        return cls._instance

    def __init__(self, repository: KakaoAuthenticationRepository = None):
        if not hasattr(self, "initialized"):
            # 의존성 주입을 원칙으로 하되, 테스트/초기화를 위해 기본값 처리 가능
            if repository:
                self.repository = repository
            self.config = get_kakao_config()
            self.initialized = True

    def generate_oauth_url(self) -> str:
        if not self.config.kakao_client_id:
            raise ValueError("KAKAO_CLIENT_ID가 설정되지 않았습니다.")
        params = urlencode({
            "client_id": self.config.kakao_client_id,
            "redirect_uri": self.config.kakao_redirect_uri,
            "response_type": "code",
        })
        return f"{self.config.KAKAO_AUTH_URL}?{params}"

    async def login_with_kakao(self, code: str) -> Dict[str, Any]:
        """
        1. 카카오 토큰 발급
        2. 카카오 사용자 정보 조회
        """
        access_token = await self.repository.fetch_access_token(code)
        if not access_token:
            raise ValueError("카카오 토큰 발급 실패")

        user_info = await self.repository.fetch_user_info(access_token)
        if not user_info:
            raise ValueError("카카오 사용자 정보 조회 실패")

        return user_info
