from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from .scraping import scraping
from .models import User
from user.models import VisitorCount
from graduation.models import Standard
from graduation.models import MyDoneLecture
from graduation.liberCheck import check_db_mydone_liber
from graduation.major_calculate import select_graduation_standard
from rest_framework.response import Response
from django.http import HttpResponse
from datetime import timedelta, datetime, timezone


@api_view(['POST'])
def student_auth(request):    # 재학생인증
    non_target = ['국어교육과', '지리교육과', '수학교육과', '체육교육과', '컴퓨터교육과', '영어교육과', '역사교육과', '자율전공학부']
    data = request.data
    studentId = data.get('studentId')
    studentPW = data.get('studentPW')
    isPasswordReset = data.get('isPasswordReset', False)    # 비밀번호 재설정
    result = scraping(studentId, studentPW)
    if isinstance(result, tuple):
        student_id, name, major = result
        if User.objects.filter(student_id = student_id, name = name).exists() and not isPasswordReset:
            error = '이미 가입된 회원입니다.'
            data = {'error' : error}
            print(f'Fail Student Auth.. \nerror: {data}')
        elif int(student_id[:4]) >= 2023 or int(student_id[:4]) <= 2017:
            error = '서비스 이용 대상이 아닙니다.'
            data = {'error' : error}
            print(f'Fail Student Auth.. \nerror: {data}')
        elif major in non_target:
            error = '서비스 이용 대상이 아닙니다.'
            data = {'error' : error}
            print(f'Fail Student Auth.. \nerror: {data}')
        else:
            data = {'student_id': student_id, 'name' : name, 'major' : major}
            print(f'Success Student Auth! \n{major} {student_id} {name}')
    else:
        error = result
        data = {'error' : error}
        print(f'Fail Student Auth.. \nerror: {data}')
    return Response (data)

@api_view(['POST'])
def register_info(request):    # 회원가입
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
                date_time_joined = (datetime.now(timezone.utc) + timedelta(hours=9)),
                name = name,
                major = major,
                student_id = student_id,
                sub_major_type = sub_major_type,
                sub_major = sub_major,
                micro_degree = micro_degree,
                password = make_password(password)
            )
            print(f'Success Sign Up! \n회원가입 일시(KST): {user.date_time_joined} \n이름: {user.name} \n전공코드: {user.major} \n학번: {user.student_id} \n비밀번호: {user.password} \n추가전공 종류: {user.sub_major_type} \n추가전공 코드: {user.sub_major} \n소단위전공: {user.micro_degree}')
            return Response (True)
        except Exception as e:
            print(f'DB 저장 오류: {repr(e)}')
            return Response (False)
    else:
        print(f'Fail Sign Up')
        return Response (False)

@api_view(['POST'])
def reset_check_register(request):  # 비밀번호 재설정 (회원 정보 확인)
    data = request.data
    student_id = data.get('studentId')
    if student_id:
        if User.objects.filter(student_id = student_id).exists():
            data = {'success' : True}
        else:
            error = '회원 정보를 찾을 수 없습니다. 회원가입을 먼저 진행해주세요.'
            data = {'error' : error}
    else:
        error = '서버가 원활하지 않습니다. 잠시 후 다시 시도해주세요.'
        data = {'error' : error}
    print(data)
    return Response (data)

@api_view(['POST'])
def check_register(request):    # 로그인
    data = request.data
    student_id = data.get('studentId')
    password = data.get('password')

    if student_id and password:
        if User.objects.filter(student_id = student_id).exists():
            user = User.objects.filter(student_id = student_id).first()
            upload_pdf = MyDoneLecture.objects.filter(user_id = student_id).exists()    # 기이수과목 DB 확인
            if user.done_major == None:
                result = {
                    "교양필수 부족 학점": None,
                    "교양선택 부족 학점": None
                }
                lack_rest_total = None,
                lack_total = None

            else:   # 졸업 검사 이력이 있다면
                result = check_db_mydone_liber(student_id)  # 교양 부족학점
                standard = select_graduation_standard(student_id) # 기준 가져오기
                standard_id = Standard.objects.filter(index = standard[-1]).first()
                if user.done_major_rest == None:
                    done_major_rest = 0
                else:
                    done_major_rest = user.done_major_rest
                if user.done_sub_major_rest == None:
                    done_sub_major_rest = 0
                else:
                    done_sub_major_rest = user.done_sub_major_rest
                if user.done_general_rest == None:
                    done_general_rest = 0
                else:
                    done_general_rest = user.done_general_rest
                if user.done_MD == None:
                    done_MD = 0
                else:
                    done_MD = user.done_MD
                if standard_id.rest_standard == None:
                    rest_standard = 0
                else:
                    rest_standard = standard_id.rest_standard

                lack_rest_total = rest_standard - (done_major_rest + done_sub_major_rest + done_general_rest + done_MD)

                if lack_rest_total < 0:
                    lack_rest_total = 0
                
                user.need_rest = lack_rest_total  # 부족한 일선 총 학점 저장
                user.save()

                if user.lack_sub_major == None:
                    lack_sub_major = 0
                else:
                    lack_sub_major = user.lack_sub_major

                lack_total = lack_rest_total + user.lack_major + user.need_general + lack_sub_major   # 부족한 학점 총계


            if check_password(password, user.password):
                user.last_login = (datetime.now(timezone.utc) + timedelta(hours=9))
                user.save()
                data = {
                    'idToken' : user.student_id,
                    'name' : user.name,
                    'testing' : user.done_major,
                    'uploadPDF' : upload_pdf,
                    'lackEssentialGE' : result.get("교양필수 부족 학점", []),
                    'lackChoiceGE' : result.get("교양선택 부족 학점", []),
                    'lackSubMajor' : user.lack_sub_major,
                    'lackRestTotal' : lack_rest_total,
                    'lackTotal' : lack_total
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
def my_info(request):    # 마이페이지
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
def remove_membership(request):    # 회원 탈퇴
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
def change_pw(request):    # 비밀번호 변경
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
def change_info(request):    # 회원정보 수정
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
        data = {'lackMajor' : user.lack_major}
    else:
        error = '회원정보를 불러오지 못했습니다. 잠시 후 다시 시도해주세요.'
        data = {'error' : error}
    print(data)
    return Response (data)

@api_view(['POST'])
def set_visitor_cookie(request):    # 방문자 수 계산
    last_visit = request.COOKIES.get('last_visit')

    response = HttpResponse("쿠키가 설정되었습니다!")

    if last_visit:
        try:
            last_visit_datetime = datetime.strptime(last_visit, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            last_visit_datetime = datetime.strptime(last_visit, '%Y-%m-%d %H:%M:%S')

        last_visit_datetime = last_visit_datetime.replace(tzinfo=timezone.utc)

        # 쿠키가 삭제가 안되었다면 삭제
        if datetime.now(timezone.utc) > last_visit_datetime + timedelta(days=1):  
            response.delete_cookie('last_visit')
            last_visit = None

    if not last_visit:
        last_visit = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')

        # 현재 UTC 시간
        now = datetime.now(timezone.utc)

        # UTC 기준 오후 3시를 생성
        afternoon_3 = now.replace(hour=15, minute=0, second=0, microsecond=0)

        # 현재 시간에 따라 만료 시간 설정
        if now < afternoon_3:
            # 오후 3시 이전이면 오늘 오후 3시로 만료 시간 설정
            expire_time = afternoon_3
        else:
            # 오후 3시 이후이면 내일 오후 3시로 만료 시간 설정
            expire_time = (afternoon_3 + timedelta(days=1))

        response.set_cookie('last_visit', last_visit, expires=expire_time, httponly=True, secure=True, samesite="None")

        visitor_entry = VisitorCount.objects.filter(id=1).first()

        visitor_entry.today_visitor += 1
        visitor_entry.total_visitor += 1
        visitor_entry.save()

    return response

@api_view(['GET'])
def get_visitor_info(request):
    visitor_data = VisitorCount.objects.first()
    
    if visitor_data:
        return Response({
            'today_visitor': visitor_data.today_visitor
        })
    else:
        return Response({'error': 'Visitor data not found'}, status=404)