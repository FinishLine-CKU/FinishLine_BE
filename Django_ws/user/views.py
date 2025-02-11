from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from .scraping import scraping
from .models import User
from graduation.models import MyDoneLecture
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
    data = request.data
    student_id = data.get('studentId')
    password = data.get('password')
    if student_id and password:
        if User.objects.filter(student_id = student_id).exists():
            user = User.objects.filter(student_id = student_id).first()
            if check_password(password, user.password):
                data = {
                    'idToken' : user.student_id,
                    'name' : user.name
                }
            else:
                error = '학번 또는 비밀번호가 올바르지 않습니다.'
                data = {'error' : error}
        else:
            error = '학번 또는 비밀번호가 올바르지 않습니다.'
            data = {'error' : error}
    else:
        error = '서버가 원활하지 않습니다. 잠시 후 다시 시도해주세요.'
        data = {'error' : error}
    print(data)
    return Response (data)

@api_view(['POST'])
def my_info(request):
    data = request.data
    student_id = data.get('idToken')
    if User.objects.filter(student_id = student_id).exists():
        user = User.objects.filter(student_id = student_id).first()
        data = {
            'major' : user.major,
            'student_id' : user.student_id,
        }
        if user.sub_major_type and user.sub_major:
            data['sub_major_type'] = user.sub_major_type
            data['sub_major'] = user.sub_major
        if user.micro_degree:
            data['micro_degree'] = user.micro_degree
    else:
        error = '해당 없음',
        data = {'error' : error}
    print(data)
    return Response (data)

@api_view(['POST'])
def remove_membership(request):
    data = request.data
    student_id = data.get('idToken')
    if User.objects.filter(student_id = student_id).exists():
        User.objects.filter(student_id = student_id).first().delete()
        MyDoneLecture.objects.filter(user_id = student_id).delete()
        data = { 'result' : True }
    else:
        data = { 'result' : False }
    print(data)
    return Response (data)

@api_view(['POST'])
def change_pw(request):
    data = request.data
    student_id = data.get('studentId')
    password = data.get('password')
    if student_id and password:
        user = User.objects.filter(student_id = student_id).first()
        user.password = make_password(password)
        user.save()
        data = {'success' : 'success'}
    else:
        error = '비밀번호 변경에 실패했습니다. 잠시 후 다시 시도해주세요.'
        data = {'error' : error}
    print(data)
    return Response (data)

@api_view(['POST'])
def change_info(request):
    data = request.data
    student_id = data.get('studentId')
    sub_major_type = data.get('sub_major_type')
    sub_major = data.get('sub_major')
    micro_degree = data.get('micro_degree')
    if student_id:
        user = User.objects.filter(student_id = student_id).first()
        user.sub_major_type = sub_major_type
        user.sub_major = sub_major
        user.micro_degree = micro_degree
        user.save()
        data = {'success' : 'success'}
    else:
        error = '회원정보 변경에 실패했습니다. 잠시 후 다시 시도해주세요.'
        data = {'error' : error}
    print(data)
    return Response (data)

@api_view(['POST'])
def lack_credit(request):
    data = request.data
    student_id = data.get('student_id')
    if student_id:
        user = User.objects.filter(student_id = student_id).first()
        data = {'need_major' : user.need_major}
    else:
        error = '회원정보를 불러오지 못했습니다. 잠시 후 다시 시도해주세요.'
        data = {'error' : error}
    print(data)
    return Response (data)