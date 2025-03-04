from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from .scraping import scraping
from .models import User
from graduation.models import Standard
from graduation.models import MyDoneLecture
from graduation.liberCheck import check_db_mydone_liber
from graduation.major_calculate import user_graduation_standard

from rest_framework.response import Response
from user.models import VisitorCount
from django.http import JsonResponse
from django.utils.timezone import now
from django.http import HttpResponse
from datetime import timedelta, datetime, timezone
import uuid
from user.models import VisitorCookie


@api_view(['POST'])
def student_auth(request):
    non_target = ['국어교육과', '지리교육과', '수학교육과', '체육교육과', '컴퓨터교육과', '영어교육과', '역사교육과', '자율전공학부']
    data = request.data
    studentId = data.get('studentId')
    studentPW = data.get('studentPW')
    result = scraping(studentId, studentPW)
    if isinstance(result, tuple):
        student_id, name, major = result
        if User.objects.filter(student_id = student_id, name = name).exists():
            error = '이미 가입된 회원입니다.'
            data = {'error' : error}          
        elif int(student_id[:4]) >= 2023 or int(student_id[:4]) <= 2017:
            error = '서비스 이용 대상이 아닙니다.'
            data = {'error' : error}
        elif major in non_target:
            error = '서비스 이용 대상이 아닙니다.'
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
            upload_pdf = MyDoneLecture.objects.filter(user_id = student_id).exists()    # 기이수과목 DB 확인
            if user.done_major == None:
                result = {
                    "교양필수 부족 학점": None,
                    "교양선택 부족 학점": None
                }
                needNormalTotalCredit = None,
                needTotalCredit = None

            else:   # 졸업 검사 이력이 있다면
                result = check_db_mydone_liber(student_id)  # 교양 부족학점
                standard = user_graduation_standard(student_id) # 기준 가져오기
                std = Standard.objects.filter(index = standard[-1]).first()
                if user.done_rest == None:
                    done_rest = 0
                else:
                    done_rest = user.done_rest
                if user.done_major_rest == None:
                    done_major_rest = 0
                else:
                    done_major_rest = user.done_major_rest
                if user.done_micro_degree == None:
                    done_micro_degree = 0
                else:
                    done_micro_degree = user.done_micro_degree
                
                needNormalTotalCredit = std.rest_credit - (done_rest + done_major_rest + done_micro_degree)
                if needNormalTotalCredit < 0:
                    needNormalTotalCredit = 0
                
                user.need_rest = needNormalTotalCredit  # 부족한 일선 총 학점 저장
                user.save()

                if user.need_sub_major == None:
                    need_sub_major = 0
                else:
                    need_sub_major = user.need_sub_major

                needTotalCredit = needNormalTotalCredit + user.need_major + user.need_general + need_sub_major   # 부족한 학점 총계


            if check_password(password, user.password):
                data = {
                    'idToken' : user.student_id,
                    'name' : user.name,
                    'testing' : user.done_major,
                    'uploadPDF' : upload_pdf,
                    'needEsseCredit' : result.get("교양필수 부족 학점", []),
                    'needChoiceCredit' : result.get("교양선택 부족 학점", []),
                    'need_sub_major' : user.need_sub_major,
                    'needNormalTotalCredit' : needNormalTotalCredit,
                    'needTotalCredit' : needTotalCredit
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

# @api_view(['POST'])
# def track_visitor(request):
#     session_key = request.COOKIES.get('sessionid')
#     print(now())
#     print(session_key)

#     if not session_key:
#         request.session.create()  # 새로운 세션 생성
#         session_key = request.session.session_key  # 세션 키를 가져옴

#     today = now().date()

#     visitor = VisitorCount.objects.filter(session_id = session_key, visit_date = today).first()

#     if not visitor:
#         VisitorCount.objects.create(session_id = session_key, visit_date = today)
        
#     total_visitors = VisitorCount.objects.count()
#     today_visitors = VisitorCount.objects.filter(visit_date = today).count()

#     data = {'total_visitors' : total_visitors, 'today_visitors' : today_visitors}
#     return Response(data)
#     session_id = 1

    # #세션 데이터의 키 값을 visited_today으로 선언을 하고
    # session_key = "visited_today"
    
    # #요청에 세션이 들어가 있는 지 확인 후 세션을 꺼냅니다
    # last_visit = request.session.get(session_key, None)

    # #요청에 세션이 있다면
    # if last_visit:
    #     #현재 접속 시간에서 3600초를 빼서 세션 기간을 구하고
    #     last_visit_time = now() - timedelta(seconds=3600)
    #     #현재 접속 시간과 마지막 접속 시간을 비교해서 마지막 접속 시간이 더 크다면 카운트하지 않습니다
    #     if last_visit >= str(last_visit_time):
    #         return JsonResponse({"message": "Already counted"}, status=200)
        
    # #DB에 넣을 날짜를 입력받습니다
    # today = now().date()
    # #DB에 해당 날짜의 컬럼이 존재한다면 조회, 아니라면 생성입니다
    # visitor_entry, created = VisitorCount.objects.get_or_create(date=today)
    # #조회나 생성 후 카운트를 하나 올립니다
    # visitor_entry.count += 1
    # #카운트만 다시 재업로드합니다
    # visitor_entry.save(update_fields=["count"])

    # #세션값을 갱신합니다(마지막 방문시간을 입력합니다)
    # request.session[session_key] = str(now())
    # #세션 만료시간을 3600초로 설정합니다
    # request.session.set_expiry(3600)

    # return JsonResponse({"message": "Visitor counted", "count": visitor_entry.count})

# @api_view(['POST'])
# def track_visitor(request):
    # 쿠키에서 'last_visit'을 확인
    # if request.COOKIES.get('last_visit') is None:  # 쿠키가 없으면
    #     today = now()
        
    #     # 쿠키 만료 시간 설정 (예: 1시간 후)
    #     expires_time = today + datetime.timedelta(days=1)

    #     # JsonResponse를 사용하여 응답 생성
    #     response = JsonResponse({'message': 'Visitor tracked successfully'})

    #     # 쿠키 설정 (expires를 사용)
    #     response.set_cookie('last_visit', 'visited', expires=expires_time)
    #     visitor_entry, created = VisitorCount.objects.get_or_create(date=today)
    #     visitor_entry.count += 1
    #     visitor_entry.save(update_fields=["count"])

    #     return response
    # else:
    #     # 이미 'last_visit' 쿠키가 존재하면
    #     return JsonResponse({'message': 'Visitor already tracked', 'last_visit': request.COOKIES['last_visit']})
@api_view(['POST'])
def track_visitor(request):
    last_visit = request.COOKIES.get('last_visit')

    response = HttpResponse("쿠키가 설정되었습니다!")

    if last_visit:
        try:
            last_visit_datetime = datetime.strptime(last_visit, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            last_visit_datetime = datetime.strptime(last_visit, '%Y-%m-%d %H:%M:%S')

        last_visit_datetime = last_visit_datetime.replace(tzinfo=timezone.utc)

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
            expire_time = (now + timedelta(days=1)).replace(hour=15, minute=0, second=0, microsecond=0)

        response.set_cookie('last_visit', last_visit, expires=expire_time, httponly=True, secure=True, samesite="None")

        today = datetime.now(timezone.utc).date()
        visitor_entry, created = VisitorCookie.objects.get_or_create(id=1)
        last_visit_datetime = datetime.strptime(last_visit, '%Y-%m-%d %H:%M:%S.%f')

        if last_visit_datetime.date() < today:
            visitor_entry.today_visitor = 1
        else:
            visitor_entry.today_visitor += 1

        visitor_entry.total_visitor += 1
        visitor_entry.save()

    return response

@api_view(['GET'])
def VisitorCookieAPI(request):
    visitor_data = VisitorCookie.objects.first()
    
    if visitor_data:
        return Response({
            'today_visitor': visitor_data.today_visitor
        })
    else:
        return Response({'error': 'Visitor data not found'}, status=404)
