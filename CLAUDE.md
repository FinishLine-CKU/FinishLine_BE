# CLAUDE.md

> 작성일 : 2026-08-14
> 대상 : Finishline_be claude 백엔드 개발 문서
> 기술 스택 : Django, Python, MySQL


## 목차
1. 핵심 설계 문서 위치
2. 기존 코드 우선 원칙
3. 코딩 컨벤션
4. 폴더 구조 규칙
5. 절대 하지 말아야 할 것

## 핵심 설계 문서 위치

- ERD/DB 설계 : docs/be/erd.md
- 기능 명세서 : docs/be/functional_spec.md
- API 명세 : docs/be/api_spec.md
- 도메인 명세(졸업요건) : docs/be/graduation_rules.md
- 파일별 역할 명세 : docs/be/project_structure.md

## 기존 코드 우선 원칙

- 새로운 코드를 작성하기 전에 관련된 기존 코드를 먼저 확인한다.
- 기존 함수, 모델, 서비스의 구조와 패턴을 우선적으로 따른다.
- 동일하거나 유사한 기능이 기존 코드에 존재한다면 재사용한다.
- 기존 구조를 변경해야 하는 경우 변경 이유와 영향을 먼저 설명한다.
- 요청하지 않은 리팩토링은 수행하지 않는다.
- 기존 코드의 단순한 스타일 문제를 임의로 수정하지 않는다.


## 코딩 컨벤션

### 용어 및 변수명

- 전공 : major
- 추가전공(복수전공/부전공) : sub_major(double, minor, linked)
- 교양 : GE
- 교양 필수 : essential GE
- 교양 선택 : choice GE
- 교양 인성 : humanism GE
- 교양 기초 : basic GE
- 교양 융합 : fusion GE
- 일반 선택 : rest
- 소단위 전공 : MD
- ~ 부족 : lack
- ~ 이수 : done
- 교양 주제 : topic
- 교양 이수구분 : type
- 기준 : standard

### 네이밍

- 파일명 : Snake case
- 폴더명 : Snake case
- 변수명 : Snake case
- 매개변수 : Snake case
- 함수명 : Snake case
- Boolean props : `is` 접두사를 사용하지 않는다.

### 코드

- 들여쓰기 : 띄어쓰기(스페이스바) 4칸 사용
- import 구문과 함수 선언 사이에는 한 줄을 띄운다.
- 함수 선언 사이에는 한 줄을 띄운다.
- export 구문은 별도 줄에 작성한다.
- 태그 문자열 리터럴 : 큰 따옴표 사용
- API 엔드 포인트 : 소문자

## 폴더 구조 규칙

- Django_ws/graduation : 전공/교양 졸업 학점 계산, 이수 과목 시각화 관련 애플리케이션
- Django_ws/user : 로그인/회원가입, 크롤링 등 회원 관련 애플리케이션
- Django_ws/manages : 사용 안함

### 절대 하지 말아야 할 것

- 하드코딩된 시크릿/비밀번호/API Key 금지
- `.env`에 저장해야 하는 민감정보를 코드에 직접 작성하지 않는다.
- 기존 migration 파일을 임의로 수정하지 않는다.
- 사용하지 않는 코드를 임의로 삭제하지 않는다.
- 요청하지 않은 리팩토링을 하지 않는다.