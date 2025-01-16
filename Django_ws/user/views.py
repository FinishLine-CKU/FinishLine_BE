from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from .scraping import scraping
from .models import User
from rest_framework.response import Response

@api_view(['POST'])
def student_auth(request):
    data = request.data
    studentId = data.get('studentId')
    studentPW = data.get('studentPW')
    result = scraping(studentId, studentPW)
    if isinstance(result, tuple):
        student_id, name, major = result
        if User.objects.filter(student_id = student_id, name = name).exists():
            error = '이미 가입된 회원입니다.'
            data = {'error' : error}          
        else:
            data = {'student_id': student_id, 'name' : name, 'major' : major}
    else:
        error = result
        data = {'error' : error}
    print(data)
    return Response (data)

@api_view(['POST'])
def register_info(request):
    data = request.data
    name = data.get('name')
    major = data.get('major')
    student_id = data.get('student_id')
    sub_major_type = data.get('additionalMajorType')
    sub_major = data.get('additionalMajor')
    micro_degree = data.get('microDegree')
    password = data.get('password')
    if name and major and student_id and password:
        try:
            user = User.objects.create(
                name = name,
                major = major,
                student_id = student_id,
                sub_major_type = sub_major_type,
                sub_major = sub_major,
                micro_degree = micro_degree,
                password = make_password(password)
            )
            print(user.name, user.major, user.student_id, user.sub_major_type, user.sub_major, user.micro_degree, user.password)
            return Response (True)
        except Exception as e:
            print(f'DB 저장 오류: {repr(e)}')
            return Response (False)
    print('회원가입 필수 데이터 누락')
    return Response (False)

@api_view(['POST'])
def check_register(request):
    return 0