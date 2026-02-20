import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.domain.auth.jwt import create_access_token
from app.domain.user.models import User
from app.kakao_authentication.service.kakao_authentication_service_impl import (
    KakaoAuthenticationServiceImpl,
)

logger = logging.getLogger(__name__)

kakao_authentication_router = APIRouter(prefix="/kakao-auth", tags=["kakao-auth"])


def inject_kakao_authentication_service() -> KakaoAuthenticationServiceImpl:
    return KakaoAuthenticationServiceImpl.get_instance()


def _upsert_user_by_kakao(
    db: Session,
    kakao_id: str,
    nickname: str | None,
    profile_image: str | None,
) -> User:
    user = db.query(User).filter(User.kakao_id == kakao_id).first()
    if user:
        user.nickname = nickname
        user.profile_image = profile_image
    else:
        user = User(kakao_id=kakao_id, nickname=nickname, profile_image=profile_image)
        db.add(user)
    db.commit()
    db.refresh(user)
    return user


@kakao_authentication_router.get("/request-oauth-link")
def request_oauth_link(
    kakao_service: KakaoAuthenticationServiceImpl = Depends(
        inject_kakao_authentication_service
    ),
):
    oauth_url = kakao_service.generate_oauth_url()
    return RedirectResponse(url=oauth_url)


@kakao_authentication_router.get("/callback")
async def callback(
    code: str = Query(...),
    db: Session = Depends(get_db),
    kakao_service: KakaoAuthenticationServiceImpl = Depends(
        inject_kakao_authentication_service
    ),
):
    try:
        login_result = await kakao_service.login_with_kakao(code)

        user = _upsert_user_by_kakao(
            db=db,
            kakao_id=login_result.user_info.kakao_id,
            nickname=login_result.user_info.nickname,
            profile_image=login_result.user_info.profile_image,
        )

        jwt_token = create_access_token(user.id, user.kakao_id)
        logger.info("카카오 로그인 성공. user_id=%s", user.id)
        return RedirectResponse(url=f"/?token={jwt_token}")
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("kakao callback failed: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error") from e

