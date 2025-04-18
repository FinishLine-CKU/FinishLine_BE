from graduation.models import Standard
from graduation.models import MyDoneLecture
from user.models import User

# 소단위전공 이수학점 계산
def pop_done_MD(student_id):
    user_MD_data = list(MyDoneLecture.objects.filter(
            lecture_type__in = ['소전'],
            user_id = student_id
        ).values_list('credit', flat=True))

    done_MD = sum(user_MD_data)
    print('소단위 전공 과목 총 이수학점: ', done_MD)

    return done_MD
    

# 학생의 졸업 기준 설정
def select_user_standard(student_id):
    user_info = User.objects.filter(student_id = student_id).values('student_id', 'major', 'sub_major_type').first()
    year = user_info['student_id'][:4]

    medical_college = ['030501*', '030503*']  # 의예과(1~2학년) / 의학과(3~6학년)
    health_care_college = ['032801*', '032802*']  # 임상병리학과 / 치위생학과
    human_service_college = ['032703*', '032705*', '032708*', '032709*', '032710*', '032702*']  # 산림치유, 언어재활, 중독재활/중독재활상담/복지상담, 통합치유/스마트통합치유, 해양치유레저, 치매전문재활
    education_college = ['030701*', '030704*', '030710*', '030709*', '030702*', '030705*', '030707*']  # 국어교육과, 수학교육과, 역사교육과, 영어교육과, 지리교육과, 체육교육과, 컴퓨터교육과

    # 18~25학년도 공통 분류
    if user_info['major'] in medical_college:
        major = '의학과'

    elif user_info['major'] == '030502*':
        major = '간호학과'

    elif user_info['major'] == '03300117':
        major = '건축학'

    # 입학년도 별 분류
    elif (int(year) <= 2021) and (user_info['major'] == '03300118'):
        major = '건축공학'

    elif int(year) >= 2023:
        if user_info['major'] == '03300101':
            major = '의료경영'
        
        elif user_info['major'] == '03300114':
            major = '항공운항'

        elif user_info['major'] == '03300115':
            major = '항공정비'

        elif user_info['major'] in health_care_college:
            major = '헬스케어융합대학'

        elif user_info['major'] in human_service_college:
            major = '휴먼서비스대학'
            # 2023 : 산림치유, 언어재활, 중독재활상담, 치매전문재활, 통합치유
            # 2024 ~ 2025 : (복지상담), (스마트통합치유), 산림치유, 언어재활, 치매전문재활, (해양치유레저)
        
        elif user_info['major'] in education_college:
            major = '사범대학'
            # 2023 ~ 2025 : 교직과, 국어교육과, 수학교육과, 역사교육과, 영어교육과, 지리교육과, 체육교육과, 컴퓨터교육과
        else:
            major = '일반학과'
    else :
        major = '일반학과'

    sub_major_type = user_info['sub_major_type']

    # 교직 복전/부전공 이수 시 졸업요건에서 소단위 전공 제외 (추후)
    if sub_major_type == '':
        sub_major_type = None

    MD_standard, rest_standard = Standard.objects.filter(year = year, college = major, sub_major_type = sub_major_type).values_list('MD_standard', 'rest_standard').first()
    
    print('소단위 전공 기준: ', MD_standard)

    return MD_standard, rest_standard

    
def calculate_lack_MD(student_id):
    standard_data = select_user_standard(student_id)

    done_MD = pop_done_MD(student_id) # 소단위전공 교과목 이수학점
    MD_standard = standard_data[0]    # 소단위전공 졸업 기준 학점
    rest_standard = standard_data[-1]    # 일반선택 졸업 기준 학점

    # 소단위전공이 졸업요건이 아닌 경우
    if MD_standard == None:
        MD_standard = 0
        lack_MD = 0
        done_MD_rest = done_MD
        User.objects.filter(student_id = student_id).update(done_MD_rest = done_MD_rest)
    
    # 졸업요건에 소단위전공이 포함된 경우 (23~25 일반학과, 사범대학)
    else:
        # 학생의 소단위 전공에 따라 졸업요건 재설정
        MD = User.objects.filter(student_id = student_id).values_list('MD', flat=True).first()

        if MD == '130':  # 지속가능발전 MD (10)
            MD_standard = 10
            rest_standard -= 1

        elif MD in ['150', '230']:  # 스마트기술창업 MD / 웰니스치유농업 MD (11)
            MD_standard = 11
            rest_standard -= 2

        elif MD in ['110', '120', '140', '141', '180', '190', '200', '210', '220', '240', '260', '280', '290', '300', '310']:  # 스마트시티 MD / 재난안전소방 MD / AI리터러시 MD / AI기반환경디자인홍보 MD / 디지털영상콘텐츠 MD / 반도체공정및장비 MD / 의료AI시스템 MD / 다문화와한국어교육 MD / 융합형사이버수사 MD / 데이터리터러시 MD / 의료데이터분석&시각화 MD / *스마트양식과식품데이터 MD / 스마트ICT융합기술 MD / 미래에너지 MD / *웰니스치유 MD (12)
            MD_standard = 12
            rest_standard -= 3

        elif MD == '270':  # *스마트푸드테크와IT MD (13)
            MD_standard = 13
            rest_standard -= 4

        elif MD in ['160', '170', '250']:  # *스포츠경영관리분석 MD / 디지털스포츠헬스케어 MD / *미래모빌리티 MD (15)
            MD_standard = 15
            rest_standard -= 6

        lack_MD = MD_standard - done_MD

        # 소단위 전공 이수학점 초과
        if lack_MD < 0:
            done_MD_rest = abs(lack_MD)
            lack_MD = 0
        
        # 소단위전공 이수학점이 부족한 경우
        else:
            done_MD_rest = 0

        User.objects.filter(student_id = student_id).update(done_MD = done_MD, done_MD_rest = done_MD_rest, lack_MD = lack_MD)

    return done_MD, done_MD_rest, MD_standard, rest_standard, lack_MD