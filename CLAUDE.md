# FinishLine_BE

FinishLine(졸업요건 확인 서비스) 백엔드. Django 프로젝트이며 코드는 `Django_ws/` 아래에 있다.

## 구조

- `Django_ws/Django_ws/settings/base.py` — 공통 설정. `production.py`는 gitignore 대상이라 저장소에 없다.
- `graduation/` — 졸업요건 계산 핵심 로직 (`GE_calculate*.py`, `major_calculate.py`, `sub_major_calculate.py`, `education_calculate.py`, `micro_degree_calculate.py`, `rest_calculate.py`, `extract.py`) 과 API(`views.py`, `serializers.py`, `urls.py`)
- `user/` — 사용자 모델/인증, 학사 정보 스크래핑(`scraping.py`), 크론 작업(`cron.py`)
- `manages/` — 관리용 앱

## 코드 리뷰 지침

- 리뷰 댓글, 요약, 제안 코드의 설명은 모두 **한국어**로 작성한다.
- 중요도 순서로 본다.
  1. 버그·로직 오류. 특히 졸업요건 계산 로직의 엣지케이스(학번/입학년도별 분기, 전공·부전공·교양 학점 경계값, 빈 데이터)
  2. 보안 — 시크릿·키 하드코딩, 인증/권한 체크 누락, 입력 검증 없이 쿼리에 사용, 민감정보 로깅
  3. ORM 성능 — 반복문 안 쿼리(N+1, `select_related`/`prefetch_related` 필요), 불필요한 전체 조회, 트랜잭션 누락
  4. 모델 변경 시 migration 누락 또는 migration과 모델 불일치
  5. serializer 검증 누락, 예외 처리 누락, 잘못된 HTTP 상태 코드
- 스타일·네이밍 같은 사소한 지적은 실제 문제로 이어질 때만, 짧게 한다.
- 확신이 없으면 단정하지 말고 질문 형태로 남긴다.
- 문제가 없으면 짧은 요약만 남기고 불필요한 칭찬은 하지 않는다.
