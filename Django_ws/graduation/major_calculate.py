'''
from graduation.models import MyDoneLecture, Standard
from user.models import User
from graduation.major_calculate import pop_user_major, user_graduation_standard, need_credit

pop_user_major()

user_graduation_standard()
'''

'''
순서

1. 기이수과목에서 전공 교과목 추출 (전필, 전선)
2. 사용자의 졸업 요건 선택 (학번, 전공, 추가전공 고려)
3. 두 값의 차이를 계산
4. User Table에 결과 저장

'''

from graduation.models import Standard
from graduation.models import MyDoneLecture
from user.models import User


# 1. 기이수 과목 (전공 추출)
# 기이수과목에서 lecture_type (이수구분) : 전필, 전선 추출

def pop_user_major(student_id):
    user_major_lectures = list(MyDoneLecture.objects.filter(
    lecture_type__in = ['전필', '전선', '전심', '전기', '기초', '공통'],
    user_id = student_id
    ).values_list('credit', flat=True))

    user_credit = sum(user_major_lectures)

    print('전공 교과목 이수학점: ', user_credit)

    return user_credit


# 2. 학생 정보 (졸업요건 조회)
# 학번 : 적용 년도 설정
# 전공 : 소속 단과대학 설정
# 복전/부전공 여부 : 일반학과 분류 시 복전/부전공 여부 확인 

def user_graduation_standard(student_id):
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
        major_standard = list(Standard.objects.filter(year = year, college = major, sub_major_type = sub_major_type).values_list('major_credit', flat=True))
        standard_id = list(Standard.objects.filter(year = year, college = major, sub_major_type = sub_major_type).values_list('index', flat=True))
        print('기준: ', major_standard[0])
        print('인덱스: ', standard_id[0])

        return major_standard[0], standard_id[0]

    else:
        standard = Standard.objects.filter(year = year, college = major, sub_major_type = sub_major_type).values('major_credit', 'sub_major_credit')
        standard_id = list(Standard.objects.filter(year = year, college = major, sub_major_type = sub_major_type).values_list('index', flat=True))
        major_standard = standard[0]['major_credit']
        sub_major_standard = standard[0]['sub_major_credit']
        print(major_standard, sub_major_standard, standard_id[0])

        return major_standard, sub_major_standard, standard_id[0]

    # Standard.objects.filter()

def need_credit(student_id):
    user_major = pop_user_major(student_id)
    standard = user_graduation_standard(student_id)
    if len(standard) == 2:
        major_standard = standard[0]
        std_id = standard[1]
        need_major = major_standard - user_major
        User.objects.filter(student_id = student_id).update(need_major = need_major, done_major = user_major)
        return need_major, user_major, std_id
    else:
        major_standard = standard[0]
        sub_major_standard = standard[1]
        std_id = standard[2]
        return major_standard, sub_major_standard, std_id
