from pydantic import BaseModel


class KakaoUserInfo(BaseModel):
    kakao_id: str
    nickname: str | None = None
    profile_image: str | None = None


class KakaoLoginResult(BaseModel):
    access_token: str
    user_info: KakaoUserInfo

