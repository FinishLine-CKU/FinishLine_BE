from graduation.models import Standard
from graduation.models import MyDoneLecture
from user.models import User

def pop_user_micro_degree(student_id):
    user_micro_degree_lectures = list(MyDoneLecture.objects.filter(
            lecture_type__in = ['소전'],
            user_id = student_id
        ).values_list('credit', flat=True))

    user_credit = sum(user_micro_degree_lectures)

    print('소단위 전공 과목 총 이수학점: ', user_credit)

    return user_credit

# 학생의 졸업 기준 가져오기
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
    micro_degree_credit = list(Standard.objects.filter(year = year, college = major, sub_major_type = sub_major_type).values_list('micro_degree_credit', flat=True))
    standard_id = list(Standard.objects.filter(year = year, college = major, sub_major_type = sub_major_type).values_list('index', flat=True))
    print('소단위 전공 기준: ', micro_degree_credit[0])
    print('인덱스: ', standard_id[0])

    return micro_degree_credit[0], standard_id[0]

    
def need_micro_degree(student_id):
    standard = user_graduation_standard(student_id) # 소단위전공 졸업 기준 
    done_micro_degree = pop_user_micro_degree(student_id) # 소단위전공 총 이수학점
    major_standard = standard[0]    # 소단위전공 기준 학점
    # if major_standard == None:
    User.objects.filter(student_id = student_id).update(done_micro_degree = done_micro_degree)

    return done_micro_degree # 전공부족학점, 전공이수학점, 졸업 요건 인덱스