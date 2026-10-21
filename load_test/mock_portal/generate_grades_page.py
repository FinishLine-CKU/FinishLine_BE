"""
docs/oneclick_load_test.md의 "교과목 리스트 예시"를 기반으로
가짜 "전체 성적조회" 페이지(pages/grades/grades.html)를 생성한다.

실제 auto_test.py가 읽는 구조를 그대로 재현한다:
  //div[@class="dataArea"]/table[3]/tbody/tr
  td[1]=이수학기(년/학기) td[2]=이수구분(전체 명칭) td[3]=이수영역/주제
  td[4]=교과목명 td[5]=학점 td[6]=등급

이수구분은 auto_test.py가 축약(전공선택→전선 등)하므로, 실제 사이트처럼
축약 전 전체 명칭으로 기록한다. 주제는 실제 사이트 형식("역량 / 주제")을
재현해 auto_test.py의 split('/', 1)[-1] 처리를 그대로 검증할 수 있게 한다.

재실행하면 pages/grades/grades.html을 덮어쓴다.

학번별 프로필 페이지 생성:
    python generate_grades_page.py --profiles <loadtest_subjects.json>
    -> json의 학번 순서대로 pages/grades/profiles/01.html ~ 을 생성한다. (server.py 참고)
    실제 학생의 이수 이력(학번만 가짜)이므로 profiles/는 git에 올리지 않는다.
"""
import json
import sys
from pathlib import Path

# (이수년도, 학기, 교과목명, 이수구분 축약형, 주제, 학점)
# docs/oneclick_load_test.md > 교과목 리스트 예시 그대로 사용
SUBJECTS = [
    (2024, 2, "삶을바꾸는구비전승의지혜-설화의재발견", "교양", "인간과문학", 2.0),
    (2024, 2, "기계학습원리와응용", "전선", "", 3.0),
    (2024, 2, "마이크로프로세서프로그래밍실무", "전선", "", 3.0),
    (2024, 2, "소프트웨어설계및개발", "전선", "", 3.0),
    (2024, 2, "고급모바일프로그래밍과실습", "전선", "", 3.0),
    (2024, 2, "고급데이터베이스구축과실무", "전선", "", 3.0),
    (2024, 2, "사제동행세미나6", "전필", "", 0.5),
    (2024, 1, "봉사와실천2", "교양", "봉사활동", 1.0),
    (2024, 1, "담바고이야기:기호품의문화적이해", "교양", "심리와건강", 2.0),
    (2024, 1, "아웃사이더,시대를앞서간사람들", "교양", "언어와문화", 2.0),
    (2024, 1, "미술문화체험", "교양", "철학과예술", 2.0),
    (2024, 1, "예술작품을통해인생과세상보기", "교양", "철학과예술", 2.0),
    (2024, 1, "빅데이터분석과활용", "전선", "", 3.0),
    (2024, 1, "고급프로그래밍실습", "전선", "", 3.0),
    (2024, 1, "자료구조및실습", "전선", "", 3.0),
    (2024, 1, "사제동행세미나5", "전필", "", 0.5),
    (2023, 2, "봉사와실천1", "교양", "봉사활동", 1.0),
    (2023, 2, "일본애니메이션과대중문화", "교양", "언어와문화", 2.0),
    (2023, 2, "달콤한식음료이야기", "교양", "역사와사회", 2.0),
    (2023, 2, "컴퓨터비전", "전선", "", 3.0),
    (2023, 2, "AI활용을위한머신러닝기초", "전선", "", 3.0),
    (2023, 2, "오라클중심의데이터베이스와실습", "전선", "", 3.0),
    (2023, 2, "자바프로그래밍과실습Ⅱ", "전선", "", 3.0),
    (2023, 2, "사제동행세미나4", "전필", "", 0.5),
    (2023, 1, "스포츠워킹", "교양", "심리와건강", 2.0),
    (2023, 1, "미디어로만나는문화와예술의기원", "교양", "철학과예술", 2.0),
    (2023, 1, "창의와상상의디자인", "교양", "철학과예술", 2.0),
    (2023, 1, "중국의인문자원과관광", "교양", "철학과예술", 2.0),
    (2023, 1, "C프로그래밍과실습II", "전선", "", 3.0),
    (2023, 1, "자바프로그래밍과실습Ⅰ", "전선", "", 3.0),
    (2023, 1, "웹프로그래밍과실습", "전선", "", 3.0),
    (2023, 1, "사제동행세미나3", "전필", "", 0.5),
    (2020, 2, "인공지능활용을위한데이터과학", "교선", "계열기초", 2.0),
    (2020, 2, "확률통계학", "교선", "균형3", 3.0),
    (2020, 2, "VERUM캠프1", "교필", "VERUM캠프", 1.0),
    (2020, 2, "VERUM캠프2", "교필", "VERUM캠프", 1.0),
    (2020, 2, "논리적사고와글쓰기", "교필", "논리적사고와글쓰기", 2.0),
    (2020, 2, "대학영어II", "교필", "외국어", 2.0),
    (2020, 2, "인간:삶의진실", "교필", "인간학", 2.0),
    (2020, 2, "소프트웨어직업탐색", "전선", "", 3.0),
    (2020, 2, "사제동행세미나2", "전필", "", 0.5),
    (2020, 2, "C프로그래밍과실습I", "전필", "", 3.0),
    (2020, 1, "창의적컴퓨팅사고를위한파이썬", "교선", "계열기초", 2.0),
    (2020, 1, "지식재산의이해", "교선", "균형2", 2.0),
    (2020, 1, "일반수학1", "교필", "MSC교과군", 3.0),
    (2020, 1, "대학영어I", "교필", "외국어", 2.0),
    (2020, 1, "인간:지혜와사랑", "교필", "인간학", 2.0),
    (2020, 1, "창의적소프트웨어설계", "전선", "", 3.0),
    (2020, 1, "문제해결기법과코딩", "전필", "", 3.0),
    (2020, 1, "사제동행세미나1", "전필", "", 0.5),
    (2019, 2, "근.현대사회개혁과개혁가들", "교선", "가치와실천", 2.0),
    (2019, 2, "아웃사이더,시대를앞서간사람들", "교선", "가치와실천", 2.0),
    (2019, 2, "미학의역사에서배우는창조정신", "교선", "상상력과표현", 2.0),
    (2019, 2, "VERUM캠프2", "교필", "VERUM캠프", 1.0),
    (2019, 2, "논리적사고와글쓰기", "교필", "논리적사고와글쓰기", 2.0),
    (2019, 2, "봉사와실천1", "교필", "봉사활동", 1.0),
    (2019, 2, "대학영어II", "교필", "외국어", 2.0),
    (2019, 2, "소프트웨어직업탐색", "전선", "", 3.0),
    (2019, 2, "사제동행세미나2", "전필", "", 0.5),
    (2019, 2, "C프로그래밍과실습I", "전필", "", 3.0),
]

# auto_test.py가 축약형으로 되돌리는 전체 명칭 (실제 사이트 표기 재현)
AREA_FULL_NAME = {
    "전선": "전공선택",
    "전필": "전공필수",
    "교필": "교양필수",
    "교선": "교양선택",
    "교양": "교양선택",  # 예시 데이터의 표기가 불분명해 교양선택으로 가정
}

# 실제 사이트의 "이수영역/주제" 원본 표기(역량 라벨 + 주제)를 재현하기 위한 라벨.
# auto_test.py는 split('/', 1)[-1]로 역량 라벨을 버리고 주제만 남긴다.
COMPETENCY_LABELS = ["정보활용", "인문소양", "글로벌역량", "창의융합", "공동체역량"]

# grade == 'N' or 'F'는 auto_test.py가 건너뛰므로, 해당 스킵 분기 검증을 위해
# 일부 과목에 F를 부여한다. (인덱스는 SUBJECTS 리스트 기준, 0부터 시작)
FAIL_GRADE_INDEXES = {6, 23}  # 사제동행세미나6, 사제동행세미나4


def build_row(index, subject):
    year, semester, name, area_short, topic, credit = subject
    area_full = AREA_FULL_NAME[area_short]
    topic_raw = f"{COMPETENCY_LABELS[index % len(COMPETENCY_LABELS)]} / {topic}" if topic else ""
    grade = "F" if index in FAIL_GRADE_INDEXES else "A+"

    return (
        "      <tr>"
        f"<td>{year}/{semester}</td>"
        f"<td>{area_full}</td>"
        f"<td>{topic_raw}</td>"
        f"<td>{name}</td>"
        f"<td>{credit}</td>"
        f"<td>{grade}</td>"
        "</tr>"
    )


# auto_test.py가 축약하는 이수구분만 전체 명칭으로 되돌린다.
# (교양, 교직처럼 축약 대상이 아닌 값은 사이트 표기 그대로 둔다)
PROFILE_AREA_FULL_NAME = {
    "전필": "전공필수", "전선": "전공선택", "교필": "교양필수", "교선": "교양선택",
    "일선": "일반선택", "소전": "소단위전공", "복전": "복수전공", "부전": "부전공",
    "연계": "연계전공", "전기": "전공기본", "전심": "전공심화", "기초": "기초전공", "공통": "공통전공",
}


def build_profile_row(index, subject):
    topic = subject["주제"].strip()
    topic_raw = f"{COMPETENCY_LABELS[index % len(COMPETENCY_LABELS)]} / {topic}" if topic else ""
    return (
        "      <tr>"
        f"<td>{subject['이수년도']}/{subject['학기']}</td>"
        f"<td>{PROFILE_AREA_FULL_NAME.get(subject['이수구분'], subject['이수구분'])}</td>"
        f"<td>{topic_raw}</td>"
        f"<td>{subject['교과목명']}</td>"
        f"<td>{subject['학점']}</td>"
        "<td>A+</td>"
        "</tr>"
    )


def build_profiles(json_path):
    with open(json_path, encoding="utf-8") as f:
        subjects = json.load(f)
    by_user = {}
    for subject in subjects:
        by_user.setdefault(subject["학번"], []).append(subject)

    out_dir = Path(__file__).parent / "pages" / "grades" / "profiles"
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.html"):
        old.unlink()
    for no, (student_id, user_subjects) in enumerate(by_user.items(), start=1):
        rows = "\n".join(build_profile_row(i, s) for i, s in enumerate(user_subjects))
        (out_dir / f"{no:02d}.html").write_text(build_html(rows), encoding="utf-8")
        print(f"generated profiles/{no:02d}.html (원본 {student_id}, {len(user_subjects)} rows)")


def build_html(rows=None):
    if rows is None:
        rows = "\n".join(build_row(i, s) for i, s in enumerate(SUBJECTS))
    return f"""<!DOCTYPE html>
<html lang="ko">
<head><meta charset="utf-8"><title>전체 성적조회 (Mock)</title></head>
<body>
<div class="dataArea">
  <table><tbody><tr><td>학생 정보 요약 (mock)</td></tr></tbody></table>
  <table><tbody><tr><td>학기별 평점 요약 (mock)</td></tr></tbody></table>
  <table>
    <thead>
      <tr><th>이수학기</th><th>이수구분</th><th>이수영역/주제</th><th>교과목명</th><th>학점</th><th>등급</th></tr>
    </thead>
    <tbody>
{rows}
    </tbody>
  </table>
</div>
</body>
</html>
"""


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--profiles":
        build_profiles(sys.argv[2])
        sys.exit()
    out_path = Path(__file__).parent / "pages" / "grades" / "grades.html"
    out_path.write_text(build_html(), encoding="utf-8")
    print(f"generated {out_path} ({len(SUBJECTS)} rows, {len(FAIL_GRADE_INDEXES)} F-grade rows)")
