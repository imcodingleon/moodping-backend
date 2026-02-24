from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import logging

from moodping.kakao_authentication.service.kakao_authentication_service_impl import KakaoAuthenticationServiceImpl
from moodping.kakao_authentication.repository.kakao_authentication_repository_impl import KakaoAuthenticationRepositoryImpl
from moodping.account.service.account_service_impl import AccountServiceImpl
from moodping.authentication.service.authentication_service_impl import AuthenticationServiceImpl
from moodping.config.settings import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])
kakao_redirect_router = APIRouter(tags=["auth"])
logger = logging.getLogger(__name__)

KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"


def get_kakao_authentication_service() -> KakaoAuthenticationServiceImpl:
    repository = KakaoAuthenticationRepositoryImpl()
    return KakaoAuthenticationServiceImpl(repository=repository)


def get_account_service() -> AccountServiceImpl:
    return AccountServiceImpl.get_instance()


def get_authentication_service() -> AuthenticationServiceImpl:
    return AuthenticationServiceImpl()


@router.get("/kakao")
def kakao_login():
    settings = get_settings()
    if not settings.kakao_client_id:
        raise HTTPException(status_code=500, detail="KAKAO_CLIENT_ID가 설정되지 않았습니다.")
    params = urlencode({
        "client_id": settings.kakao_client_id,
        "redirect_uri": settings.kakao_redirect_uri,
        "response_type": "code",
    })
    return RedirectResponse(url=f"{KAKAO_AUTH_URL}?{params}")


@router.get("/callback")
@router.get("/kakao/callback")
async def kakao_callback(
    code: str = Query(...),
    kakao_auth_service: KakaoAuthenticationServiceImpl = Depends(get_kakao_authentication_service),
    account_service: AccountServiceImpl = Depends(get_account_service),
    authentication_service: AuthenticationServiceImpl = Depends(get_authentication_service),
):
    try:
        kakao_user_info = await kakao_auth_service.login_with_kakao(code)

        account = account_service.upsert_by_kakao(
            kakao_id=kakao_user_info["kakao_id"],
            nickname=kakao_user_info.get("nickname"),
            profile_image=kakao_user_info.get("profile_image"),
        )

        jwt_token = authentication_service.create_session(
            user_id=account.id,
            kakao_id=account.kakao_id,
        )

        logger.info("카카오 로그인 성공. user_id=%s, nickname=%s", account.id, account.nickname)
        return RedirectResponse(url=f"/?token={jwt_token}")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"카카오 로그인 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="서버 내부 오류")


@kakao_redirect_router.get("/kakao-authentication/request-access-token-after-redirection")
async def kakao_redirect_callback(
    code: str = Query(...),
    kakao_auth_service: KakaoAuthenticationServiceImpl = Depends(get_kakao_authentication_service),
    account_service: AccountServiceImpl = Depends(get_account_service),
    authentication_service: AuthenticationServiceImpl = Depends(get_authentication_service),
):
    return await kakao_callback(
        code=code,
        kakao_auth_service=kakao_auth_service,
        account_service=account_service,
        authentication_service=authentication_service,
    )
