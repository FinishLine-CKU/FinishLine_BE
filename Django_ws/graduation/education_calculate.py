from graduation.models import Standard
from graduation.models import MyDoneLecture
from user.models import User

def pop_user_education(student_id):
    user_education_data = list(MyDoneLecture.objects.filter(
        lecture_type__in = ['교직'],
        user_id = student_id
    ).values_list('credit', flat=True))

    done_education = sum(user_education_data)

    print('교직 합계:', done_education)

    return done_education

def calculate_lack_education(student_id):
    done_education = pop_user_education(student_id)

    if done_education > 0: #교직 이수 한 번이라도 교직 과목을 수강 했다면?
        done_education_rest = done_education
        lack_education = 22 - done_education_rest

        if lack_education < 0:
            done_education_rest = abs(lack_education)
            lack_education = 0
    
    else: #교직을 이수하지 않았다면
        done_education_rest = 0
        lack_education = 0

    return done_education_rest, lack_education