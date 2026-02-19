import jwt as pyjwt
from fastapi import APIRouter, Depends, HTTPException, Header

from account.service.account_service_impl import AccountServiceImpl
from config.settings import get_settings

account_router = APIRouter(prefix="/account", tags=["account"])


def inject_account_service() -> AccountServiceImpl:
    return AccountServiceImpl.get_instance()


def get_current_account_id(authorization: str | None = Header(None)) -> int:
    """Bearer 토큰에서 account_id를 추출하는 의존성 함수.
    MP-04 authentication 도메인 완성 후 AuthenticationService.validate_session()으로 교체 예정.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="인증이 필요합니다. Bearer 토큰을 전달해주세요.")

    token = authorization[7:]
    settings = get_settings()

    try:
        payload = pyjwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except pyjwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다.")
    except pyjwt.PyJWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    account_id = payload.get("sub")
    if not account_id:
        raise HTTPException(status_code=401, detail="토큰에 사용자 정보가 없습니다.")

    return int(account_id)


@account_router.get("/me")
def get_me(
    account_id: int = Depends(get_current_account_id),
    account_service: AccountServiceImpl = Depends(inject_account_service),
):
    account = account_service.find_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="계정을 찾을 수 없습니다.")

    return {
        "id": account.id,
        "kakao_id": account.kakao_id,
        "nickname": account.nickname,
        "profile_image": account.profile_image,
    }
