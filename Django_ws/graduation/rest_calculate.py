# 기이수과목에서 '일선' 교과목 추출
# major_calculate에 전달

from graduation.models import MyDoneLecture


def pop_rest_credit(student_id):
    user_major_lectures = list(MyDoneLecture.objects.filter(
    lecture_type__in = ['일선'],
    user_id = student_id
    ).values_list('credit', flat=True))

    user_credit = sum(user_major_lectures)

    print('일선 분류 과목 총 이수학점: ', user_credit)

    return user_credit