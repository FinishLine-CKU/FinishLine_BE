# 1. 기이수과목에서 전공 교과목 추출 (전필, 전선)
# 2. 사용자의 졸업 요건 선택 (학번, 전공, 추가전공 고려)
# 3. 두 값의 차이를 계산
# 4. User Table에 결과 저장

from graduation.models import Standard
from graduation.models import MyDoneLecture
from user.models import User
from graduation.rest_calculate import pop_rest_credit


# 1. 기이수 과목 (전공 추출)
# 기이수과목에서 lecture_type (이수구분) : 전필, 전선 추출

def pop_user_major(student_id):
    user_major_lectures = list(MyDoneLecture.objects.filter(
        lecture_type__in = ['전필', '전선', '전심', '전기', '기초', '공통'],
        user_id = student_id
    ).values_list('credit', flat=True))

    user_credit = sum(user_major_lectures)

    print('전공 과목 총 이수학점: ', user_credit)

    return user_credit


# 2. 학생 정보 (졸업요건 조회)
# 학번 : 적용 년도 설정
# 전공 : 소속 단과대학 설정
# 복전/부전공 여부 : 일반학과 분류 시 복전/부전공 여부 확인 

def select_graduation_standard(student_id):
    user_info = User.objects.filter(student_id = student_id).values('student_id', 'major', 'sub_major_type')
    year = user_info[0]['student_id'][:4]
    if (user_info[0]['major'] == '030501*') or (user_info[0]['major'] == '030503*'):
        major = '의학과'
    elif (user_info[0]['major'] == '030502*'):
        major = '간호학과'
    elif (user_info[0]['major'] == '03300118'):
        major = '건축공학'
    elif (user_info[0]['major'] == '03300117'):
        major = '건축학'
    else :
        major = '일반학과'

    sub_major_type = user_info[0]['sub_major_type']
    if sub_major_type == '':
        sub_major_type = None

    major_standard, standard_id = Standard.objects.filter(year = year, college = major, sub_major_type = sub_major_type).values_list('major_standard', 'index').first()
    return major_standard, standard_id


def calculate_major(student_id):
    done_major = pop_user_major(student_id) # 전공 총 이수학점
    major_standard, standard_id = select_graduation_standard(student_id)
    done_rest = pop_rest_credit(student_id) # 일선 총 이수학점

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
