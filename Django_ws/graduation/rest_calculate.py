# 기이수과목에서 '일선' 교과목 추출
# major_calculate에 전달

from graduation.models import MyDoneLecture


def pop_done_rest(student_id):
    user_rest_data = list(MyDoneLecture.objects.filter(
        lecture_type__in = ['일선'],
        user_id = student_id
    ).values_list('credit', flat=True))

    done_rest = sum(user_rest_data)

    print('일반선택 과목합계:', done_rest)

    return done_rest