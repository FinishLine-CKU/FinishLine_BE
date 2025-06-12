from graduation.models import Standard
from graduation.models import MyDoneLecture
from user.models import User

def pop_user_education(student_id):
    user_education_data = list(MyDoneLecture.objects.filter(
        lecture_type__in = ['교직'],
        user_id = student_id
    ).values_list('credit', flat=True))

    done_education_rest = sum(user_education_data)

    print('교직 합계:', done_education_rest)

    return done_education_rest

def calculate_lack_education(student_id):
    done_education_rest = pop_user_education(student_id)

    # 교직 교과목 수강 이력 존재하는 경우
    if done_education_rest > 0:
        lack_education = 22 - done_education_rest

        if lack_education < 0:
            lack_education = 0
        
        User.objects.filter(student_id = student_id).update(done_education_rest = done_education_rest, lack_education = lack_education)
    
    else:
        done_education_rest = 0
        lack_education = 0
        
    return done_education_rest, lack_education