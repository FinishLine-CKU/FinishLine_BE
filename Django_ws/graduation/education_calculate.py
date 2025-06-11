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

def select_user_standard(student_id):
    user_info = User.objects.filter(student_id = student_id).values('student_id', 'major', 'sub_major_type').first()
    year = user_info['student_id'][:4]
    
    education_college = ['030701*', '030704*', '030710*', '030709*', '030702*', '030705*', '030707*']  # 국어교육과, 수학교육과, 역사교육과, 영어교육과, 지리교육과, 체육교육과, 컴퓨터교육과

    if user_info['major'] in education_college:
        major = user_info['major']
        sub_major_type = user_info['sub_major_type']
        # education_standard = Standard.objects.filter(year = year, college = major, sub_major_type = sub_major_type).values_list('education_standard').first()
        education_standard = 22
    
    else:
        education_standard = 0

    return education_standard

def calculate_lack_education(student_id):
    done_education = pop_user_education(student_id)
    education_standard = select_user_standard(student_id)

    if education_standard == 0:
        done_education = 0
        education_standard = 0
        lack_education = 0
    else:
        lack_education = education_standard - done_education

    if lack_education < 0:
        lack_education = 0

    return education_standard, done_education, lack_education