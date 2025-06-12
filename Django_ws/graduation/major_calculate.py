# 1. 기이수과목에서 전공 교과목 추출 (전필, 전선)
# 2. 사용자의 졸업 요건 선택 (학번, 전공, 추가전공 고려)
# 3. 두 값의 차이를 계산
# 4. User Table에 결과 저장

from graduation.models import Standard
from graduation.models import MyDoneLecture
from user.models import User
from graduation.rest_calculate import pop_done_rest


# 1. 기이수 과목 (전공 추출)
# 기이수과목에서 lecture_type (이수구분) : 전필, 전선 추출

def pop_user_major(student_id):
    user_major_data = list(MyDoneLecture.objects.filter(
        lecture_type__in = ['전필', '전선', '전심', '전기', '기초', '공통'],
        user_id = student_id
    ).values_list('credit', flat=True))

    done_major = sum(user_major_data)

    print('전공 합계:', done_major)

    return done_major


# 2. 학생 정보 (졸업요건 조회)
# 학번 : 적용 년도 설정
# 전공 : 소속 단과대학 설정
# 복전/부전공 여부 : 일반학과 분류 시 복전/부전공 여부 확인 

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

    elif user_info['major'] in education_college:
        major = '사범대학'
        # 2023 ~ 2025 : 교직과, 국어교육과, 수학교육과, 역사교육과, 영어교육과, 지리교육과, 체육교육과, 컴퓨터교육과

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
    
        else:
            major = '일반학과'
    else :
        major = '일반학과'

    sub_major_type = user_info['sub_major_type']

    # 교직 복전/부전공 이수 시 졸업요건에서 소단위 전공 제외 (추후)
    if sub_major_type == '':
        sub_major_type = None

    major_standard, standard_id = Standard.objects.filter(year = year, college = major, sub_major_type = sub_major_type).values_list('major_standard', 'index').first()

    return major_standard, standard_id


def calculate_major(student_id):
    done_major = pop_user_major(student_id) # 전공 총 이수학점
    major_standard, standard_id = select_user_standard(student_id)
    done_rest = pop_done_rest(student_id) # 일선 총 이수학점

    lack_major = major_standard - done_major
    done_major_rest = 0

    # 전공 이수 학점을 초과 하여 이수한 경우 (= 전공 졸업요건 초과)
    if lack_major < 0:
        done_major_rest = abs(lack_major)   # 전공에서 일선으로 빠지는 학점
        lack_major = 0
        
    User.objects.filter(student_id = student_id).update(
        done_major = done_major,
        done_major_rest = done_major_rest,
        lack_major = lack_major,
        done_rest = done_rest)

    return lack_major, done_major, standard_id  # 전공부족학점, 전공이수학점, 졸업 요건 인덱스
