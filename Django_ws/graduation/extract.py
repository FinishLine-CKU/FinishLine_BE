from django.shortcuts import render
from django.http import HttpResponse
import pdfplumber
import re
from .models import MyDoneLecture
from .models import AllLectureData
from user.models import MajorAlias

def extract_from_pdf_title(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

        match = re.search(r'(\d{4})\s*-\s*(\d)\s*학기', text)
        if match:
            year = match.group(1)
            semester = match.group(2)
            return year, semester
        else:
            return None, None

#전공 -> 전공코드 (major_alias 테이블 조회)
def get_major_code(major_name):
    major_alias = MajorAlias.objects.filter(alias=major_name).first()
    return major_alias.major_code if major_alias else None

# 학교 개설강좌 원천 데이터 자체가 로마숫자(Ⅰ~Ⅷ)와 라틴 문자(I~VIII) 표기를
# 규칙 없이 섞어 쓴다(같은 과목코드의 분반끼리도 표기가 다른 경우 존재).
# DB의 lecture_name 원본은 그대로 두고, 비교 시점에만 정규화해 매칭 실패를 막는다.
ROMAN_TO_LATIN_NUMERAL = {
    'Ⅰ': 'I', 'Ⅱ': 'II', 'Ⅲ': 'III', 'Ⅳ': 'IV',
    'Ⅴ': 'V', 'Ⅵ': 'VI', 'Ⅶ': 'VII', 'Ⅷ': 'VIII',
}

def normalize_lecture_name(lecture_name):
    if not lecture_name:
        return lecture_name
    normalized = lecture_name
    for roman, latin in ROMAN_TO_LATIN_NUMERAL.items():
        normalized = normalized.replace(roman, latin)
    return normalized

# lecture_name 완전일치 대신 정규화한 이름으로 비교해 후보를 찾는다.
def find_matching_lecture_by_name(queryset, lecture_name):
    target = normalize_lecture_name(lecture_name)
    for lecture in queryset:
        if normalize_lecture_name(lecture.lecture_name) == target:
            return lecture
    return None

def lecture_name_matches_any(lecture_name, name_list):
    target = normalize_lecture_name(lecture_name)
    return any(normalize_lecture_name(name) == target for name in name_list)

#학과, 전공, 학번 추출
def extract_major_from_pdf_table(uploaded_file):
    uploaded_file.seek(0)  
    with pdfplumber.open(uploaded_file) as pdf:
        major_data = None  
        student_year = None
        for page in pdf.pages:
            table = page.extract_table()

            if table is None:
                raise ValueError("PDF 형식 오류: 이미지 기반 PDF")

            for i in table:
                print(i)

            if table:
                for row in table:
                    if "학과/전공" in row and row[3]:
                        major_data = row[3].strip()
                        break

                for row in table:
                    if "학 번" in row and row[3]:
                        student_year = row[3][:4].strip()
                        break

            if major_data is None or student_year is None:
                raise ValueError("PDF 형식 오류: pdf Nonetype")
                

    major_code = get_major_code(major_data)

    print(f"추출된 학과: {major_data} → 변환된 코드: {major_code}")
    return major_code, student_year

#과목 목록 추출
def extract_from_pdf_table(user_id, uploaded_file):
    year, semester = extract_from_pdf_title(uploaded_file)
    
    uploaded_file.seek(0)
    
    with pdfplumber.open(uploaded_file) as pdf:
        table_data = []
        for page in pdf.pages:
            table = page.extract_table()
                
            if table:
                for row in table:
                    if row[0] and row[0] in ["교양", "전필", "전선", "소전", "복전", "부전", "연계", "교필", "교선", "전공선택", "전공필수",
                                                                    "전공", "전심", "기초", "일선", "일반선택", "공통", "공통전공", "전공기본",
                                                                    "전공심화", "기초전공", "전기", "교직"]:
                        grade = row[9].strip() if row[9] else "" 

                        if grade in ["N", "F"]:
                            continue
                        
                        #추출한 과목을 정해진 형식으로 저장
                        subject_data = {
                            '이수년도': year,
                            '학기': semester,
                            '이수구분': row[0],
                            '주제': row[1].split('/', 1)[-1].strip() if row[1].strip() else ' ',
                            '교과목명': row[4],
                            '학점': row[7],
                            '학번': user_id
                        }
                        table_data.append(subject_data)
            
            else:
                raise ValueError("PDF 형식 오류: 이미지 기반 PDF")
            
        if len(table_data) == 0:
            raise ValueError("PDF 형식 오류: 과목 추출 불가")

    return table_data

#전체 과목 데이터에서 과목코드를 가져와 내 기이수 과목에 저장
def save_pdf_data_to_db(subjects_data, student_year, major=None):
    saved_subjects = []
    duplicate_subjects = []

    for subject in subjects_data:
        # 중복 데이터 (lecture_name은 로마숫자/라틴 정규화 후 비교)
        existing_lecture_names = MyDoneLecture.objects.filter(
            year=subject['이수년도'],
            semester=subject['학기'],
            user_id=subject['학번'],
        ).values_list('lecture_name', flat=True)

        if lecture_name_matches_any(subject['교과목명'], existing_lecture_names):
            print(f"Check Duplicate Subject: {subject['학번']} {major if major else '-'} 교과목명: {subject['교과목명']}")
            duplicate_subjects.append(subject)
            continue

        # 학생 기이수과목 - 강의 DB 매칭 & 이수영역 전처리
        else:
            # 기이수과목 - 강의 DB 매칭 (lecture_name은 로마숫자/라틴 정규화 후 비교)
            if "사제동행세미나" in subject['교과목명'] and major:
                change_major_code = major[0] if isinstance(major, list) else major

                matching_alllecture = find_matching_lecture_by_name(
                    AllLectureData.objects.filter(
                        year=subject['이수년도'],
                        semester=subject['학기'],
                        major_code=change_major_code
                    ),
                    subject['교과목명']
                )

            elif '복전' in subject['이수구분']:
                matching_alllecture = find_matching_lecture_by_name(
                    AllLectureData.objects.filter(
                          year=subject['이수년도'],
                          semester=subject['학기'],
                          credit=subject['학점'],
                    ),
                    subject['교과목명']
                )

            elif '부전' in subject['이수구분']:
                matching_alllecture = find_matching_lecture_by_name(
                    AllLectureData.objects.filter(
                          year=subject['이수년도'],
                          semester=subject['학기'],
                          credit=subject['학점'],
                    ),
                    subject['교과목명']
                )

            elif '일선' in subject['이수구분']:
                matching_alllecture = find_matching_lecture_by_name(
                    AllLectureData.objects.filter(
                          year=subject['이수년도'],
                          semester=subject['학기'],
                          credit=subject['학점'],
                    ),
                    subject['교과목명']
                )

            else:
                matching_alllecture = find_matching_lecture_by_name(
                    AllLectureData.objects.filter(
                        year=subject['이수년도'],
                        semester=subject['학기'],
                        lecture_type=subject['이수구분'],
                        credit=subject['학점'],
                    ),
                    subject['교과목명']
                )

            if subject['이수구분'] in ['교필', '교양'] and subject['주제'] in [' ', '', '인성', 'MSC교과']:
                lecture_name = subject['교과목명']
                if lecture_name_matches_any(lecture_name, AllLectureData.objects.filter(lecture_topic__icontains = '외국어').values_list('lecture_name', flat=True).distinct()):
                    subject['주제'] = '외국어'
                elif lecture_name_matches_any(lecture_name, AllLectureData.objects.filter(lecture_topic__icontains = '인간학').values_list('lecture_name', flat=True).distinct()):
                    if '철학적인간학' in lecture_name:
                        subject['주제'] = '철학적인간학'
                    elif '신학적인간학' in lecture_name:
                        subject['주제'] = '신학적인간학'
                    else:
                        subject['주제'] = '인간학'
                elif lecture_name_matches_any(lecture_name, AllLectureData.objects.filter(lecture_topic__startswith = 'VERUM').values_list('lecture_name', flat=True).distinct()):
                    subject['주제'] = 'VERUM캠프'
                elif lecture_name_matches_any(lecture_name, AllLectureData.objects.filter(lecture_topic__startswith = '봉사').values_list('lecture_name', flat=True).distinct()):
                    subject['주제'] = '봉사활동'
                elif '논리적사고와글쓰기' in lecture_name:
                    subject['주제'] = '논리적사고와글쓰기'
                elif '창의적사고와코딩' in lecture_name:
                    if student_year in ['2018', '2019']:
                        subject['주제'] = '창의적사고와코딩'
                    elif student_year in ['2020', '2021', '2022']:
                        subject['주제'] = 'MSC교과군'
                elif lecture_name_matches_any(lecture_name, AllLectureData.objects.filter(lecture_topic = 'MSC교과군').values_list('lecture_name', flat=True).distinct()):
                    subject['주제'] = 'MSC교과군'

            #내 기이수 과목에 저장
            if matching_alllecture:
                subject_instance = MyDoneLecture(
                    year=subject['이수년도'],
                    semester=subject['학기'],
                    lecture_type=subject['이수구분'],
                    lecture_topic=subject['주제'],
                    lecture_name=subject['교과목명'],
                    credit=subject['학점'],
                    lecture_code=matching_alllecture.lecture_code,
                    alllecture=matching_alllecture,
                    user_id=subject['학번'],
                )
                subject_instance.save()
                saved_subjects.append(subject_instance)
                print(f"Saved to DB: {subject['학번']} {major if major else '-'} 교과목명: {subject['교과목명']}")
            else:
                print(f"Fail save to DB: {subject['학번']} 이수년도: {subject['이수년도']} 학기: {subject['학기']} 이수구분: {subject['이수구분']} 교과목명: {subject['교과목명']}")
                continue

    return saved_subjects, duplicate_subjects