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
    
    medical_college = ['030501*', '030503*']  
    health_care_college = ['032801*', '032802*'] 
    human_service_college = ['032703*', '032705*', '032708*', '032709*', '032710*', '032702*'] 
    education_college = ['030701*', '030704*', '030710*', '030709*', '030702*', '030705*', '030707*']

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

    education_standard = Standard.objects.filter(year = year, college = major, sub_major_type = sub_major_type).values_list('education_standard', flat=True).first()

    return education_standard

def calculate_lack_education(student_id):
    done_education = pop_user_education(student_id)
    education_standard = select_user_standard(student_id)

    # 비 사범대학
    if education_standard == None:
        education_standard = 0
        lack_education = 0
        done_education_rest = done_education
        User.objects.filter(student_id = student_id).update(done_education_rest = done_education_rest)

    # 사범대학
    else:
        lack_education = education_standard - done_education
        done_education_rest = 0

        if lack_education < 0:
            done_education_rest = abs(lack_education)
            lack_education = 0

        User.objects.filter(student_id = student_id).update(
            done_education = done_education,
            done_education_rest = done_education_rest,
            lack_education = lack_education
        )

    return done_education, done_education_rest, education_standard, lack_education