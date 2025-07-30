from django.shortcuts import render
from django.http import HttpResponse
import pdfplumber
import re
from .models import MyDoneLecture
from .models import AllLectureData

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
        
#전공 -> 전공코드(변경 학과명 추가)
MAJOR_MAP = {
    '의예과': '030503*',
    '간호학과': '030502*',
    '의학과': '030503*',
    '국어교육과': '030701*',
    '지리교육과': '030702*',
    '수학교육과': '030704*',
    '체육교육과': '030705*',
    '컴퓨터교육과': '030707*',
    '영어교육과': '030709*',
    '역사교육과': '030710*',
    '관광경영학과': '031103*',
    '스포츠건강관리학과': '03300111',
    '트리니티융합-스포츠재활의학전공': '03300111',
    '트리니티융합 스포츠재활의학전공': '03300111',
    '트리니티자유 스포츠재활의학전공': '03300111',
    '트리니티융합-스포츠건강관리학전공': '03300111',
    '트리니티융합 스포츠건강관리학전공': '03300111',
    '트리니티자유 스포츠건강관리학전공': '03300111',
    '호텔경영학과': '03300108',
    '트리니티융합-호텔경영학전공': '03300108',
    '트리니티융합 호텔경영학전공': '03300108',
    '트리니티자유 호텔경영학전공': '03300108',
    '트리니티융합-호텔관광경영학과': '03300108',
    '트리니티융합 호텔관광경영학과': '03300108',
    '트리니티자유 호텔관광경영학과': '03300108',
    '스포츠레저학과': '03300110',
    '트리니티융합-스포츠레저학전공': '03300110',
    '트리니티융합 스포츠레저학전공': '03300110',
    '트리니티자유 스포츠레저학전공': '03300110',
    '스포츠지도학과': '03300112',
    '트리니티융합-스포츠지도학전공': '03300112',
    '트리니티융합 스포츠지도학전공': '03300112',
    '트리니티자유 스포츠지도학전공': '03300112',
    '스포츠레저학부': '03300112',
    '스포츠레저학부-경기지도학전공': '03300112',
    '스포츠레저학부 경기지도학전공': '03300112',
    '스포테인먼트전공(F)': '031191*',
    '조리외식경영학과': '03300109',
    '트리니티융합-조리외식경영학전공': '03300109',
    '트리니티융합 조리외식경영학전공': '03300109',
    '트리니티자유 조리외식경영학전공': '03300109',
    '건축학부': '03300118',
    '건축학부-건축공학': '03300118',
    '건축학부 건축공학': '03300118',
    '건축학부 건축학전공': '03300117',
    '건축학부-건축학': '03300117',
    '건축학부 건축학': '03300117',
    '트리니티융합-건축공학전공': '03300118',
    '트리니티융합 건축공학전공': '03300118',
    '트리니티자유 건축공학전공': '03300118',
    '트리니티융합-건축학전공': '03300117',
    '트리니티융합 건축학전공': '03300117',
    '트리니티자유 건축학전공': '03300117',
    '토목공학과': '031214*',
    '전자공학과': '031224*',
    '소프트웨어학과': '031230*',
    '기술창업학과': '031241*',
    'AI융합전공(C)': '031295*',
    'AI융합전공(F)': '031297*',
    '항만물류시스템전공': '031298*',
    '반도체융합전공': '031299*',
    '사회복지학과': '03300105',
    '트리니티융합-사회복지학전공': '03300105',
    '트리니티융합 사회복지학전공': '03300105',
    '트리니티자유 사회복지학전공': '03300105',
    '경영학과': '03300106',
    '트리니티융합-경영학전공': '03300106',
    '트리니티융합 경영학전공': '03300106',
    '트리니티자유 경영학전공': '03300106',
    '광고홍보학과': '03300107',
    '트리니티융합-광고홍보학전공': '03300107',
    '트리니티융합 광고홍보학전공': '03300107',
    '트리니티자유 광고홍보학전공': '03300107',
    '경찰행정학부': '03301001',
    '경찰행정학과': '03301001',
    '경찰행정학부-경찰행정학': '03301001',
    '경찰행정학부 경찰행정학': '03301001',
    '경찰행정학부-해양경찰': '03301002',
    '경찰행정학부 해양경찰': '03301002',
    '경찰행정학부-경찰행정학전공': '03301001',
    '경찰행정학부 경찰행정학전공': '03301001',
    '경찰행정학부-해양경찰전공': '03301002',
    '경찰행정학부 해양경찰전공': '03301002',
    '경찰학부-경찰행정학': '03301001',
    '경찰학부 경찰행정학': '03301001',
    '경찰학부-해양경찰': '03301002',
    '경찰학부 해양경찰': '03301002',
    '경찰공공행정학부-공공행정학전공': '03301004',
    '경찰공공행정학부 공공행정학전공': '03301004',
    '경찰공공행정학부-경찰행정학전공': '03301001',
    '경찰공공행정학부 경찰행정학전공': '03301001',
    '트리니티융합 경찰행정학전공': '03301001',
    '트리니티자유 경찰행정학전공': '03301001',
    '트리니티융합 해양경찰학전공': '03301002',
    '트리니티자유 해양경찰학전공': '03301002',
    '행정학과': '03300104',
    '트리티니융합-행정학전공': '03300104',
    '트리티니융합 행정학전공': '03300104',
    '트리티니자유 행정학전공': '03300104',
    '스타트업콘텐츠마케팅전공(F)-스타트업콘텐츠마케팅': '032391*',
    '스타트업콘텐츠마케팅전공(F) 스타트업콘텐츠마케팅': '032391*',
    '의료공학과': '032401*',
    '트리니티융합-디지털헬스케어전공': '032401*',
    '트리니티융합 디지털헬스케어전공': '032401*',
    '트리니티자유 디지털헬스케어전공': '032401*',
    '디지털헬스케어융합전공': '032401*',
    '의료IT학과': '032402*',
    '의생명과학과': '032403*',
    '트리니티융합-의생명과학과': '032403*',
    '트리니티융합 의생명과학과': '032403*',
    '트리니티자유 의생명과학과': '032403*',
    '트리니티융합-바이오메디컬전공': '032403*',
    '트리니티융합 바이오메디컬전공': '032403*',
    '트리니티자유 바이오메디컬전공': '032403*',
    '의료경영학과': '03300101',
    '트리니티융합-의료경영학전공': '03300101',
    '트리니티융합 의료경영학전공': '03300101',
    '트리니티자유 의료경영학전공': '03300101',
    '바이오융합공학과': '032408*',
    '안경광학과': '032415*',
    '정밀의료융합전공': '032490*',
    '스마트수소에너지융합전공': '032492*',
    '항공운항서비스학과': '032501*',
    '항공경영학과': '032506*',
    '항공경영물류학과': '032506*',
    '항공교통물류학과': '032506*',
    '트리니티융합-항공교통물류전공': '032506*',
    '트리니티융합 항공교통물류전공': '032506*',
    '트리니티자유 항공교통물류전공': '032506*',
    '항공운항학과': '03300114',
    '트리니티융합-항공운항전공': '03300114',
    '트리니티융합 항공운항전공': '03300114',
    '트리니티자유 항공운항전공': '03300114',
    '무인항공학과': '032515*',
    '항공정비학과': '03300115',
    '트리니티융합-항공정비학전공': '03300115',
    '트리니티융합 항공정비학전공': '03300115',
    '트리니티자유 항공정비학전공': '03300115',
    '항공설계전공(F-C)': '032591*',
    '공연예술학부': '03260103',
    '공연예술학부-실용음악': '03260103',
    '공연예술학부 실용음악': '03260103',
    '트리니티융합-실용음악전공': '03260103',
    '트리니티융합 실용음악전공': '03260103',
    '트리니티자유 실용음악전공': '03260103',
    '공연예술학부-연기예술': '03260104',
    '공연예술학부 연기예술': '03260104',
    '공연예술학부-방송연예': '03260104',
    '공연예술학부 방송연예': '03260104',
    '뷰티디자인학과': '032603*',
    '뷰티디자인학과-뷰티디자인': '032603*',
    '뷰티디자인학과 뷰티디자인': '032603*',
    '콘텐츠제작학과': '032608*',
    '트리니티융합-콘텐츠제작전공': '032608*',
    '트리니티융합 콘텐츠제작전공': '032608*',
    '트리니티자유 콘텐츠제작전공': '032608*',
    'CG디자인학과': '032609*',
    '트리니티융합-CG디자인전공': '032609*',
    '트리니티융합 CG디자인전공': '032609*',
    '트리니티자유 CG디자인전공': '032609*',
    '미디어콘텐츠학부 CG디자인전공': '032609*',
    '치매전문재활학과': '032702*',
    '산림치유학과': '032703*',
    '언어재활학과': '032705*',
    '중독재활학과': '032708*',
    '중독재활상담학과': '032708*',
    '복지상담학과': '032708*',
    '통합치유학과': '032709*',
    '스마트통합치유학과': '032709*',
    '해양치유레저학과': '032710*',
    '임상병리학과': '032801*',
    '치위생학과': '032802*',
    '트리니티자유-반려동물학전공': '03290112',
    '트리니티자유 반려동물학전공': '03290112',
    '트리니티자유-군사학전공': '03290113',
    '트리니티자유 군사학전공': '03290113',
    '트리니티융합-스마트항만공학': '03300116',
    '트리니티융합 스마트항만공학': '03300116',
    '자율전공학부': '033020',
    }

def get_major_code(major_name):
    return MAJOR_MAP.get(major_name, None)

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
                            '주제': row[1] if row[1].strip() else ' ',
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
        # 중복 데이터
        if MyDoneLecture.objects.filter(
            year=subject['이수년도'],
            semester=subject['학기'],
            lecture_name=subject['교과목명'],
            lecture_type=subject['이수구분'],
            user_id=subject['학번'],
        ).exists():
            print(f"Check Duplicate Subject: {subject['학번']} {major if major else '-'} 교과목명: {subject['교과목명']}")
            duplicate_subjects.append(subject)
            continue 

        # 학생 기이수과목 - 강의 DB 매칭 & 이수영역 전처리
        else:
            # 기이수과목 - 강의 DB 매칭
            if "사제동행세미나" in subject['교과목명'] and major:
                change_major_code = major[0] if isinstance(major, list) else major 

                matching_alllecture = AllLectureData.objects.filter(
                    year=subject['이수년도'],
                    semester=subject['학기'],
                    lecture_name=subject['교과목명'],
                    major_code=change_major_code
                ).first()
                
            elif '복전' in subject['이수구분']:
                matching_alllecture = AllLectureData.objects.filter(
                      year=subject['이수년도'],
                      semester=subject['학기'],
                      lecture_name=subject['교과목명'],
                      credit=subject['학점'],
                ).first()

            elif '부전' in subject['이수구분']:
                matching_alllecture = AllLectureData.objects.filter(
                      year=subject['이수년도'],
                      semester=subject['학기'],
                      lecture_name=subject['교과목명'],
                      credit=subject['학점'],
                ).first()

            elif '일선' in subject['이수구분']:
                matching_alllecture = AllLectureData.objects.filter(
                      year=subject['이수년도'],
                      semester=subject['학기'],
                      lecture_name=subject['교과목명'],
                      credit=subject['학점'],
                ).first()

            else:
                matching_alllecture = AllLectureData.objects.filter(
                    year=subject['이수년도'],
                    semester=subject['학기'],
                    lecture_type=subject['이수구분'],
                    lecture_name=subject['교과목명'],
                    credit=subject['학점'],
                ).first()

            if subject['이수구분'] in ['교필', '교양'] and subject['주제'] == ' ':
                lecture_name = subject['교과목명']
                if lecture_name in AllLectureData.objects.filter(lecture_topic__icontains = '외국어').values_list('lecture_name', flat=True).distinct():
                    subject['주제'] = '외국어' 
                elif lecture_name in AllLectureData.objects.filter(lecture_topic__icontains = '인간학').values_list('lecture_name', flat=True).distinct():
                    if '철학적인간학' in lecture_name:
                        subject['주제'] = '철학적인간학'
                    elif '신학적인간학' in lecture_name:
                        subject['주제'] = '신학적인간학'
                    else:
                        subject['주제'] = '인간학'
                elif lecture_name in AllLectureData.objects.filter(lecture_topic__startswith = 'VERUM').values_list('lecture_name', flat=True).distinct():
                    subject['주제'] = 'VERUM캠프'
                elif lecture_name in AllLectureData.objects.filter(lecture_topic__startswith = '봉사').values_list('lecture_name', flat=True).distinct():
                    subject['주제'] = '봉사활동'
                elif '논리적사고와글쓰기' in lecture_name:
                    subject['주제'] = '논리적사고와글쓰기'
                elif '창의적사고와코딩' in lecture_name:
                    if student_year in ['2018', '2019']:
                        subject['주제'] = '창의적사고와코딩'
                    elif student_year in ['2020', '2021', '2022']:
                        subject['주제'] = 'MSC교과군'
                elif lecture_name in AllLectureData.objects.filter(lecture_topic = 'MSC교과군').values_list('lecture_name', flat=True).distinct():
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