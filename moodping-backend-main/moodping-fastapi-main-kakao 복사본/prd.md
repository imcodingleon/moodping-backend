현재 (바이브코딩)                   강사님 방식
─────────────────────────────────────────────────
domain/auth/router.py         →   controller/auth_controller.py
domain/auth/service.py        →   service/auth_service.py (ABC)
(함수 모음)                      service/auth_service_impl.py (Singleton)
(없음)                      →   repository/auth_repository.py (ABC)
repository/auth_repository_impl.py (Singleton)
domain/auth/schemas.py        →   controller/request/ (도메인별 분리)
domain/user/models.py         →   domain/entity/user.py (비즈니스 로직 포함)

moodping/
│
├── [main.py](http://main.py/)                              ← router 등록만
├── config/
│   ├── [settings.py](http://settings.py/)                      ← 기존 [config.py](http://config.py/)
│   └── mysql_config.py                  ← 기존 [database.py](http://database.py/)
│
├── kakao_authentication/                ★ 카카오 OAuth 전담
│   ├── controller/
│   │   ├── kakao_authentication_controller.py
│   │   └── request/
│   ├── service/
│   │   ├── kakao_authentication_service.py         ← ABC
│   │   └── kakao_authentication_service_impl.py    ← Singleton
│   ├── repository/
│   │   ├── kakao_authentication_repository.py      ← ABC
│   │   └── kakao_authentication_repository_impl.py ← httpx로 카카오 API 통신
│   └── config/
│       └── kakao_config.py
│
├── authentication/                      ★ JWT 세션 관리
│   ├── controller/
│   │   └── authentication_controller.py
│   ├── service/
│   │   ├── authentication_service.py               ← ABC
│   │   └── authentication_service_impl.py          ← JWT 생성/검증
│   └── jwt/
│       └── jwt_handler.py
│
├── account/                             ★ 사용자 엔티티 관리
│   ├── controller/
│   │   ├── account_controller.py
│   │   └── request/
│   │       └── link_anon_request.py
│   ├── service/
│   │   ├── account_service.py                      ← ABC
│   │   └── account_service_impl.py                 ← upsert, find
│   ├── repository/
│   │   ├── account_repository.py                   ← ABC
│   │   └── account_repository_impl.py
│   └── domain/
│       └── entity/
│           └── [account.py](http://account.py/)                          ← User 엔티티
│
├── mood_record/                         ★ 감정 기록
│   ├── controller/
│   │   ├── mood_record_controller.py
│   │   └── request/
│   │       └── create_mood_record_request.py
│   ├── service/
│   │   ├── mood_record_service.py                  ← ABC
│   │   └── mood_record_service_impl.py             ← save, link_anon
│   ├── repository/
│   │   ├── mood_record_repository.py               ← ABC
│   │   └── mood_record_repository_impl.py          ← find_by_user, find_7days
│   └── domain/
│       └── entity/
│           └── mood_record.py
│
├── mood_analysis/                       ★ LLM 감정 분석
│   ├── controller/
│   │   └── mood_analysis_controller.py
│   ├── service/
│   │   ├── mood_analysis_service.py                ← ABC
│   │   └── mood_analysis_service_impl.py           ← LLM 호출 + 파싱 + 저장
│   ├── repository/
│   │   ├── mood_analysis_repository.py             ← ABC
│   │   └── mood_analysis_repository_impl.py
│   ├── domain/
│   │   └── entity/
│   │       └── mood_analysis.py
│   └── prompt/
│       └── mood_analysis_prompt.py
│
├── weekly_report/                       ★ 주간 리포트
│   ├── controller/
│   │   └── weekly_report_controller.py
│   ├── service/
│   │   ├── weekly_report_service.py                ← ABC
│   │   └── weekly_report_service_impl.py           ← 7일 데이터 → LLM
│   ├── repository/
│   │   ├── weekly_report_repository.py             ← ABC
│   │   └── weekly_report_repository_impl.py
│   ├── domain/
│   │   └── entity/
│   │       └── weekly_report.py
│   └── prompt/
│       └── report_prompt.py
│
├── event_log/                           ★ 이벤트 추적
│   ├── controller/
│   │   └── event_log_controller.py
│   ├── service/
│   │   ├── event_log_service.py                    ← ABC
│   │   └── event_log_service_impl.py
│   ├── repository/
│   │   ├── event_log_repository.py                 ← ABC
│   │   └── event_log_repository_impl.py
│   └── domain/
│       └── entity/
│           └── event_log.py
│
└── llm/                                 ← 현행 유지 (이미 완벽)
├── [base.py](http://base.py/)
├── [factory.py](http://factory.py/)
├── openai_client.py
├── gemini_client.py
└── claude_client.py

[카카오 로그인 요청]
│
▼
kakao_authentication/controller
└──▶ kakao_authentication/service  (카카오 API 통신)
└──▶ account/service               (사용자 조회/생성)
└──▶ authentication/service        (JWT 발급)
└──▶ mood_record/service           (anon→user 승계 트리거)

[감정 기록 요청]
│
▼
mood_record/controller
└──▶ authentication/service        (JWT 검증 → user_id)
└──▶ mood_record/service           (저장)
└──▶ mood_analysis/service         (LLM 분석)
└──▶ llm/factory         (LLM 클라이언트)

[주간 리포트 요청]
│
▼
weekly_report/controller
└──▶ authentication/service        (JWT 검증)
└──▶ mood_record/repository        (7일치 데이터 조회)
└──▶ weekly_report/service         (리포트 생성)
└──▶ llm/factory         (LLM 요약)

<aside>
🎧

┌─────────────────────────────────────────────────────┐
│  [MP-00] 프로젝트 스캐폴딩 + 공통 인프라 설정        │
│  담당: 팀장                                          │
│  우선순위: 🔴 Critical                               │
│                                                      │
│  작업 내용:                                          │
│  - [ ] config/settings.py 생성 (기존 [config.py](http://config.py/) 이전) │
│  - [ ] config/mysql_config.py 생성 ([database.py](http://database.py/) 이전)│
│  - [ ] [main.py](http://main.py/) 뼈대 생성 (router 등록부만)           │
│  - [ ] .cursor/rules 작성 (아키텍처 규칙)            │
│  - [ ] 각 도메인 폴더 + **init**.py 빈 파일 생성     │
│                                                      │
│  의존성: 없음                                        │
│  예상 시간: 2시간                                    │
└─────────────────────────────────────────────────────┘

</aside>

┌─────────────────────────────────────────────────────┐
│  [MP-01] account 도메인 생성                         │
│  담당: 개발자 A                                      │
│  우선순위: 🔴 Critical                               │
│                                                      │
│  생성 파일:                                          │
│  - [ ] account/domain/entity/account.py              │
│        (User → Account 이름 변경)                    │
│        필드: id, kakao_id, nickname, profile_image   │
│        create() classmethod에 유효성 검사 포함       │
│  - [ ] account/repository/account_repository.py (ABC)│
│        메서드: find_by_kakao_id, save, find_by_id    │
│  - [ ] account/repository/account_repository_impl.py │
│        (Singleton)                                   │
│  - [ ] account/service/account_service.py (ABC)      │
│        메서드: upsert_by_kakao, find_by_id           │
│  - [ ] account/service/account_service_impl.py       │
│        (Singleton)                                   │
│  - [ ] account/controller/account_controller.py      │
│        GET /account/me                               │
│  - [ ] main.py에 account_router 등록                 │
│                                                      │
│  참고: 강사님 account/ 폴더 구조 그대로 따를 것      │
│  의존성: MP-00 완료 후                               │
│  예상 시간: 3시간                                    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  [MP-02] mood_record 도메인 생성                     │
│  담당: 개발자 B                                      │
│  우선순위: 🔴 Critical                               │
│                                                      │
│  생성 파일:                                          │
│  - [ ] mood_record/domain/entity/mood_record.py      │
│        create() classmethod:                         │
│        - mood_emoji 빈 문자열 불가                   │
│        - intensity 0~10 범위 검증                    │
│        - mood_text 500자 초과 불가                   │
│  - [ ] mood_record/repository/                       │
│        mood_record_repository.py (ABC)               │
│        메서드: save, find_by_id, find_by_user,       │
│               find_7days_by_user, link_anon_to_user  │
│  - [ ] mood_record/repository/                       │
│        mood_record_repository_impl.py (Singleton)    │
│  - [ ] mood_record/service/                          │
│        mood_record_service.py (ABC)                  │
│  - [ ] mood_record/service/                          │
│        mood_record_service_impl.py (Singleton)       │
│  - [ ] mood_record/controller/request/               │
│        create_mood_record_request.py                 │
│  - [ ] mood_record/controller/                       │
│        mood_record_controller.py                     │
│        POST /mood-record/create                      │
│        GET  /mood-record/list                        │
│  - [ ] main.py에 mood_record_router 등록             │
│                                                      │
│  참고: 강사님 board/ 구조를 mood_record에 적용       │
│  의존성: MP-00 완료 후                               │
│  예상 시간: 4시간                                    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  [MP-03] event_log 도메인 생성                       │
│  담당: 개발자 C                                      │
│  우선순위: 🟡 Medium                                 │
│                                                      │
│  생성 파일:                                          │
│  - [ ] event_log/domain/entity/event_log.py          │
│  - [ ] event_log/repository/                         │
│        event_log_repository.py (ABC)                 │
│        event_log_repository_impl.py (Singleton)      │
│  - [ ] event_log/service/                            │
│        event_log_service.py (ABC)                    │
│        event_log_service_impl.py (Singleton)         │
│  - [ ] event_log/controller/                         │
│        event_log_controller.py                       │
│        POST /event-log/create                        │
│        GET  /event-log/metrics                       │
│  - [ ] main.py에 event_log_router 등록               │
│                                                      │
│  의존성: MP-00 완료 후                               │
│  예상 시간: 2시간                                    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  [MP-04] authentication 도메인 생성 (JWT)            │
│  담당: 개발자 A                                      │
│  우선순위: 🔴 Critical                               │
│                                                      │
│  생성 파일:                                          │
│  - [ ] authentication/jwt/jwt_handler.py             │
│        create_access_token, decode_token             │
│  - [ ] authentication/service/                       │
│        authentication_service.py (ABC)               │
│        메서드: create_session, validate_session       │
│  - [ ] authentication/service/                       │
│        authentication_service_impl.py (Singleton)    │
│  - [ ] authentication/controller/                    │
│        authentication_controller.py                  │
│        GET /auth/me (현재 로그인 사용자 정보)        │
│  - [ ] main.py에 authentication_router 등록          │
│                                                      │
│  비즈니스 규칙:                                      │
│  - JWT 만료: 7일 (10080분)                           │
│  - Payload: sub(user_id), kakao_id, exp              │
│                                                      │
│  의존성: MP-01 (account 도메인 필요)                 │
│  예상 시간: 3시간                                    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  [MP-05] kakao_authentication 도메인 생성            │
│  담당: 개발자 B                                      │
│  우선순위: 🔴 Critical                               │
│                                                      │
│  생성 파일:                                          │
│  - [ ] kakao_authentication/config/kakao_config.py   │
│  - [ ] kakao_authentication/repository/              │
│        kakao_authentication_repository.py (ABC)      │
│        메서드: fetch_access_token, fetch_user_info   │
│  - [ ] kakao_authentication/repository/              │
│        kakao_authentication_repository_impl.py       │
│        (Singleton, httpx로 카카오 API 통신)          │
│  - [ ] kakao_authentication/service/                 │
│        kakao_authentication_service.py (ABC)         │
│        메서드: generate_oauth_url, login_with_kakao  │
│  - [ ] kakao_authentication/service/                 │
│        kakao_authentication_service_impl.py          │
│        (Singleton)                                   │
│  - [ ] kakao_authentication/controller/              │
│        kakao_authentication_controller.py            │
│        GET /kakao-auth/request-oauth-link            │
│        GET /kakao-auth/callback                      │
│  - [ ] main.py에 kakao_authentication_router 등록    │
│                                                      │
│  흐름:                                               │
│  Controller에서 3개 서비스 조합:                     │
│   1. kakao_auth_service → 카카오 로그인              │
│   2. account_service → 사용자 조회/생성              │
│   3. authentication_service → JWT 발급               │
│   4. mood_record_service → anon 승계 (선택)          │
│                                                      │
│  참고: 강사님 kakao_authentication/ 구조 그대로      │
│  의존성: MP-01, MP-04 완료 후                        │
│  예상 시간: 4시간                                    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  [MP-06] mood_analysis 도메인 생성                   │
│  담당: 개발자 C                                      │
│  우선순위: 🟡 Medium                                 │
│                                                      │
│  생성 파일:                                          │
│  - [ ] mood_analysis/domain/entity/mood_analysis.py  │
│  - [ ] mood_analysis/repository/ (ABC + Impl)        │
│  - [ ] mood_analysis/service/ (ABC + Impl)           │
│        메서드: analyze_and_save(record) → LLM 호출   │
│  - [ ] mood_analysis/prompt/mood_analysis_prompt.py  │
│  - [ ] mood_analysis/controller/                     │
│        mood_analysis_controller.py (필요시)          │
│                                                      │
│  핵심: llm/factory.get_llm_client() 재사용           │
│  의존성: MP-02 완료 후                               │
│  예상 시간: 3시간                                    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  [MP-07] weekly_report 도메인 생성                   │
│  담당: 개발자 A                                      │
│  우선순위: 🟡 Medium                                 │
│                                                      │
│  생성 파일:                                          │
│  - [ ] weekly_report/domain/entity/weekly_report.py  │
│  - [ ] weekly_report/repository/ (ABC + Impl)        │
│        메서드: find_by_user_and_week, save           │
│  - [ ] weekly_report/service/ (ABC + Impl)           │
│        메서드: get_or_create_latest_report           │
│        → mood_record/repository에서 7일치 조회       │
│        → llm/ 으로 요약 생성                         │
│  - [ ] weekly_report/prompt/report_prompt.py         │
│  - [ ] weekly_report/controller/                     │
│        weekly_report_controller.py                   │
│        GET /weekly-report/latest                     │
│  - [ ] main.py에 weekly_report_router 등록           │
│                                                      │
│  Cross-Domain 의존:                                  │
│   - mood_record/repository (7일 데이터 조회)         │
│   - llm/factory (LLM 요약)                           │
│   - authentication/service (JWT 검증)                │
│                                                      │
│  의존성: MP-02, MP-04, MP-06 완료 후                 │
│  예상 시간: 4시간                                    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  [MP-08] 레거시 코드 제거 + 통합 테스트              │
│  담당: 전원                                          │
│  우선순위: 🟢 Low                                    │
│                                                      │
│  - [ ] app/routers/ (레거시) 폴더 삭제               │
│  - [ ] app/services/ (레거시) 폴더 삭제              │
│  - [ ] app/models.py, app/schemas.py 삭제            │
│  - [ ] app/deps.py → authentication 도메인으로 이전  │
│  - [ ] [main.py](http://main.py/) 최종 정리                             │
│  - [ ] 전체 API 엔드포인트 동작 확인                 │
│  - [ ] 카카오 로그인 → 감정 기록 → 분석 E2E 테스트  │
│                                                      │
│  의존성: MP-01~07 전부 완료 후                       │
│  예상 시간: 2시간                                    │
└─────────────────────────────────────────────────────┘

```
    개발자 A          개발자 B          개발자 C
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sprint 0  [MP-00 팀장이 인프라 세팅]
────────────────────────────────────────────
Sprint 1  MP-01 account   MP-02 mood_record  MP-03 event_log
(3h)            (4h)               (2h)
────────────────────────────────────────────
Sprint 2  MP-04 auth(JWT) MP-05 kakao_auth   MP-06 mood_analysis
(3h)            (4h)               (3h)
────────────────────────────────────────────
Sprint 3  MP-07 weekly_report
(4h)
────────────────────────────────────────────
Sprint 4  [MP-08 전원 통합 + 레거시 제거]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
총 10h          총 8h             총 5h

## **핵심 포인트**

**충돌 제로 설계**: Sprint 1에서 A/B/C가 각각 account/, mood_record/, event_log/ 를 만드니까 **같은 파일을 건드리는 일이 없습니다.**

**Cursor 프롬프트 사용법**: 각 티켓을 받은 팀원은 Cursor에 이렇게 입력하면 됩니다.

아래 티켓을 기반으로 account 도메인을 구현해줘.

[티켓 내용 붙여넣기]

반드시 .cursor/rules의 아키텍처 규칙을 따르고,

강사님 프로젝트의 board/ 폴더 구조를 참고해서 만들어.

기존 파일([main.py](http://main.py/) 제외)은 수정하지 마.