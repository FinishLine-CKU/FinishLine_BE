from django.shortcuts import render
from django.http import HttpResponse
import pdfplumber
import re
from .models import MyDoneLecture
from .models import AllLectureData
import math

def extract_from_pdf_title(pdf_stream):
    with pdfplumber.open(pdf_stream) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

        match = re.search(r'(\d{4})\s*-\s*(\d)\s*학기', text)
        if match:
            year = match.group(1)
            semester = match.group(2)
            return year, semester
        else:
            return None, None

def extract_from_pdf_table(pdf_stream):
    year, semester = extract_from_pdf_title(pdf_stream)
    
    pdf_stream.seek(0)
    
    with pdfplumber.open(pdf_stream) as pdf:
        table_data = []
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table:
                    if any(subject_type in row for subject_type in ["교양", "전필", "전선", "소전", "교필", "교선", "전공선택", "전공필수"]):
                        subject_data = {
                            '이수년도': year,
                            '학기': semester,
                            '이수구분': row[0],
                            '주제': row[1] if row[1].strip() else ' ',
                            '교과목명': row[4],
                            '학점': row[7],
                            '등급': row[9],
                        }
                        table_data.append(subject_data)
                        print(subject_data)
    return table_data

def save_pdf_data_to_db(subjects_data):
    saved_subjects = []

    lecture_type_mapping = {
        '교선': '교선',  # 예시로 교양을 교선으로 매핑
        '교필': '교필',
        '교양': '교양',
        '전공': '전공',
        '공전': '공통전공',
        '전선': '전공선택',
        '전필': '전공필수',
        '전심': '전공심화',
        '기전': '기초전공',
        '전기': '전공기본',
        '소전': '소단위전공',
        '일선': '일반선택',
        # 추가적인 매핑이 필요하면 여기에 추가
    }

    for subject in subjects_data:
        mapped_lecture_type = lecture_type_mapping.get(subject['이수구분'], subject['이수구분'])
        # 중복된 과목이 MyDoneLecture에 있는지 확인
        print(f"Mapped Lecture Type: {mapped_lecture_type}")
        if MyDoneLecture.objects.filter(
            year=subject['이수년도'],
            semester=subject['학기'],
            lecture_name=subject['교과목명'],
            lecture_type=mapped_lecture_type
        ).exists():
            continue
        else:
            # AllLectureData에서 해당 과목명, 이수구분, 이수영역이 일치하는 과목을 찾음
            matching_alllecture = AllLectureData.objects.filter(
                year=subject['이수년도'],
                semester=subject['학기'],
                lecture_type=mapped_lecture_type,
                lecture_topic=subject['주제'],
                lecture_name=subject['교과목명'],
                credit=subject['학점'],
            ).first()

            # 일치하는 과목이 있을 경우
            if matching_alllecture:
                subject_instance = MyDoneLecture(
                    year=subject['이수년도'],
                    semester=subject['학기'],
                    lecture_type=mapped_lecture_type,
                    lecture_topic=subject['주제'],
                    lecture_name=subject['교과목명'],
                    credit=subject['학점'],
                    grade=subject['등급'],
                    # AllLectureData에서 과목코드를 가져와서 MyDoneLecture에 저장
                    lecture_code=matching_alllecture.lecture_code,
                    alllecture=matching_alllecture
                )
            else:
                print(f"No matching AllLectureData found for: {subject['교과목명']}")
                continue

            # MyDoneLecture에 저장
            subject_instance.save()
            saved_subjects.append(subject_instance)

    return saved_subjects