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