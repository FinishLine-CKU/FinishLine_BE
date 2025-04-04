from user.models import User
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.response import Response
from io import BytesIO
from .extract import extract_from_pdf_table
from .extract import save_pdf_data_to_db
from .extract import extract_major_from_pdf_table
from .liberCheck import check_db_mydone_liber
import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import MyDoneLecture
from .models import Standard
from .models import AllLectureData
from .models import NowLectureData
from .serializers import MyDoneLectureSerializer
from .serializers import AllLectureDataSerializer
from .serializers import NowLectureDataSerializer
from .major_calculate import need_credit
from .micro_degree_calculate import need_micro_degree
import io

logger = logging.getLogger(__name__)

#내 기이수 과목 데이터 학번으로 조회
class MyDoneLectureModelViewSet(ModelViewSet):
    queryset = MyDoneLecture.objects.all()
    serializer_class = MyDoneLectureSerializer
    
    #GET 요청
    def list(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')  # 쿼리 파라미터에서 user_id 가져오기
        if not user_id:
            return Response({"detail": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = MyDoneLecture.objects.filter(user_id=user_id).order_by('-year', '-semester')
        serializer = MyDoneLectureSerializer(queryset, many=True)
        return Response(serializer.data)
    
    #POST 요청
    def create(self, request, *args, **kwargs):
        if isinstance(request.data, dict) and 'subjectsToSave' in request.data:
            subjects = request.data['subjectsToSave']

            user_id = subjects[0]['user_id']

            for subject in subjects:
                lecture_code = subject['lecture_code'] 
                user_major_code = User.objects.filter(student_id=user_id).values('major').first()
                user_sub_major_type = User.objects.filter(student_id=user_id).values('sub_major_type').first()
                user_sub_major = User.objects.filter(student_id=user_id).values('sub_major').first()
                subject_major_code = NowLectureData.objects.filter(lecture_code=lecture_code).values('major_code').first()
                print('과목찾기 : ', user_id, user_major_code, user_sub_major_type, user_sub_major['sub_major'])
                if(subject_major_code['major_code'] == " "):
                    print(user_id, "교양 추가 : ", lecture_code)
                    break

                elif(user_major_code['major'] == subject_major_code['major_code']):
                    print('과목찾기 : ', user_id, "전공 추가 : ", lecture_code)
                    break

                elif(user_sub_major_type['sub_major_type']):
                    user_sub_major_type_data = user_sub_major_type['sub_major_type']

                    if(user_sub_major_type_data == 'double'):
                        if(user_sub_major['sub_major'] == subject_major_code['major_code']):
                            subject['lecture_type'] = '복전'
                            print('과목찾기 : ', user_id, "복전으로 변경 : ",  lecture_code, subject_major_code)

                        else:
                            subject['lecture_type'] = '일선'
                            print('과목찾기 : ', user_id, "일선으로 변경 : ", lecture_code, subject_major_code)

                    elif(user_sub_major_type_data == 'minor'):
                        if(user_sub_major['sub_major'] == subject_major_code['major_code']):
                            subject['lecture_type'] = '부전'
                            print('과목찾기 : ', user_id, "복전으로 변경 : ", lecture_code, subject_major_code)
                        else:
                            subject['lecture_type'] = '일선'
                            print('과목찾기 : ', user_id, "일선으로 변경 : ", lecture_code, subject_major_code)

                    elif(user_sub_major_type_data == 'linked'):
                        if(user_sub_major['sub_major'] == subject_major_code['major_code']):
                            subject['lecture_type'] = '연계'
                            print('과목찾기 : ', user_id, "연계전공으로 변경 : ", lecture_code, subject_major_code)
                        else:
                            subject['lecture_type'] = '일선'
                            print('과목찾기 : ', user_id, "일선으로 변경 : ", lecture_code, subject_major_code)
                    
                    else:
                        subject['lecture_type'] = '일선'
                        print('과목찾기 : ', user_id, "일선으로 변경 : ", lecture_code, subject_major_code)

                else:
                    subject['lecture_type'] = '일선'

            serializer = self.get_serializer(data=subjects, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return super().create(request, *args, **kwargs)
        
    #DELETE 요청
    def destroy(self, request, *args, **kwargs):
        lecture_code = kwargs.get('pk')
        user_id = request.data.get('user_id')

        if not user_id or not lecture_code:
            return Response({'detail': 'user_id and lecture_code are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        subject = MyDoneLecture.objects.filter(user_id=user_id, lecture_code=lecture_code).first()

        if not subject:
            print(f"delete요청 에러 사용자: {user_id}, {lecture_code}")
            return Response({'detail': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
        
        subject.delete()

        return Response(
            {"detail": f"Lecture {lecture_code} deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

#전체과목 데이터 조회
class AllLectureDataModelViewSet(ModelViewSet):
    queryset = AllLectureData.objects.all()
    serializer_class = AllLectureDataSerializer

    @action(detail=False, methods=['get'], url_path='filter-by-code/(?P<lectureCode>[^/.]+)')
    def filter_by_code(self, request, lectureCode=None): 
        
        if len(lectureCode) > 9:
            lectureCode
        else:
            lectureCode = lectureCode[:6] + "-" + lectureCode[6:9]
            
        queryset = AllLectureData.objects.filter(lecture_code=lectureCode)
        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)
    
#과목코드로 조회
class NowLectureModelViewSet(ModelViewSet):
    queryset = NowLectureData.objects.all()
    serializer_class = NowLectureDataSerializer

    @action(detail=False, methods=['get'], url_path='filter-by-code/(?P<lectureCode>[^/.]+)')
    def filter_by_code(self, request, lectureCode=None): 
        
        if len(lectureCode) > 9:
            lectureCode
        else:
            lectureCode = lectureCode[:6] + "-" + lectureCode[6:9]
            
        queryset = NowLectureData.objects.filter(lecture_code=lectureCode)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

#pdf에서 정보 추출
@api_view(['POST'])
def upload_pdf(request):
    if 'files' not in request.FILES:
        return Response({'error': 'No file uploaded'}, status=400)

    user_id = request.data.get('user_id')
    files = request.FILES.getlist('files')
    result_data = []
    duplicate_files = []

    #요청에 .pdf로 끝나는 file이 존재한다면
    for uploaded_file in files:
        if uploaded_file.name.endswith('.pdf'):
            try:
                # pdf_bytes = io.BytesIO()

                #메모리 효율을 위해 chunks로 나누어 분석
                # for chunk in uploaded_file.chunks():
                #     pdf_bytes.write(chunk)

                uploaded_file.seek(0)

                print("사용자:", user_id, "PDF 추출 로직 시작")

                #학번과 전공을 추출
                extracted_major, student_year = extract_major_from_pdf_table(uploaded_file)

                #pdf내부 과목목록을 추출
                extracted_table = extract_from_pdf_table(user_id, uploaded_file)

                #DB에 이수영역 변경 후 저장
                saved_subjects = save_pdf_data_to_db(extracted_table, student_year, extracted_major)

                # pdf_bytes.close()

                if saved_subjects: 
                    result_data.append({
                        'file': uploaded_file.name,
                        'status': 'saved',
                        'message': f"File '{uploaded_file.name}' uploaded successfully."
                    })
                else:
                    duplicate_files.append(uploaded_file.name)

            except MemoryError:
                logger.error("메모리 부족 오류 발생 - 업로드 중단")
                return Response({'error': '사용자가 많아 업로드할 수 없습니다. 잠시 후 다시 시도해 주세요.'}, status=500)

            except Exception as e:
                logger.error(f"Error processing file {uploaded_file.name}: {str(e)}")
                return Response({'error': f'Error processing file {uploaded_file.name}: {str(e)}'}, status=500)
            
    logger.info("File processing completed.")
    print(result_data)
    return Response({
        'message': 'Files processed successfully',
        'data': result_data,
        'duplicate_files': duplicate_files,
    })

#졸업요건 검사 결과 전달
@api_view(['POST'])
def general_check(request):
    user_id = request.data.get('user_id')

    # print(f"Received user_id: {user_id}")
    result = check_db_mydone_liber(user_id) 
    print(result)

    return Response({
        'message': 'Files processed successfully',
        'general_data': {
            '교양필수_부족_학점': result.get("교양필수 부족 학점", []), #
            '교양선택_부족_학점': result.get("교양선택 부족 학점", []), #
            '교양필수_부족_영역': result.get("교양필수 부족 영역", []), 
            '교양선택_부족_영역': result.get("교양선택 부족 영역", []), 
            '교양필수_이수_학점': result.get("교양필수 이수 학점", []), 
            '교양선택_이수_학점': result.get("교양선택 이수 학점", []), 
            '일반선택_이수_학점': result.get("일반선택 이수 학점", []), 
        }
    })

@api_view(['POST'])
def test_major(request):
    data = request.data
    student_id = data.get('student_id')
    result = need_credit(student_id)
    if len(result) == 4:
        need_major, user_major, id, need_sub_major = need_credit(student_id)
        major = User.objects.filter(student_id = student_id).values_list('major', flat=True)
        done_major_rest = User.objects.filter(student_id = student_id).values_list('done_major_rest', flat=True)
        done_rest = User.objects.filter(student_id = student_id).values_list('done_rest', flat=True)
        gradu = Standard.objects.filter(index = id).first()

        if gradu.rest_credit == None:
            data = {
                'major_info' : major[0], # 전공
                'need_major' : need_major, # 부족학점
                'user_major' : user_major, # 이수한 학점
                'total_credit' : gradu.total_credit, # 졸업 총 학점
                'major_credit' : gradu.major_credit, # 전공 총 학점
                'general_essential_credit' : gradu.general_essential_credit, # 교양필수 총 학점
                'general_selection_credit' : gradu.general_selection_credit, # 교양필수 총 학점
                'rest_credit' : 0,
                'done_major_rest' : done_major_rest[0],
                'need_sub_major' : need_sub_major,
                'done_rest' : done_rest[0]
            },
        else:
            data = {
                'major_info' : major[0], # 전공
                'need_major' : need_major, # 부족학점
                'user_major' : user_major, # 이수한 학점
                'total_credit' : gradu.total_credit, # 졸업 총 학점
                'major_credit' : gradu.major_credit, # 전공 총 학점
                'general_essential_credit' : gradu.general_essential_credit, # 교양필수 총 학점
                'general_selection_credit' : gradu.general_selection_credit, # 교양필수 총 학점
                'rest_credit' : gradu.rest_credit,
                'done_major_rest' : done_major_rest[0],
                'need_sub_major' : need_sub_major,
                'done_rest' : done_rest[0]
            }
    else:
        # 추가 전공자 결과 반환
        need_major, user_major, id, need_sub_major, user_sub_major = need_credit(student_id)
        major = User.objects.filter(student_id = student_id).values_list('major', flat=True)
        done_major_rest = User.objects.filter(student_id = student_id).values_list('done_major_rest', flat=True)
        done_rest = User.objects.filter(student_id = student_id).values_list('done_rest', flat=True)
        gradu = Standard.objects.filter(index = id).first()

        # 의학과, 간호학과, 건축학, 건축공학 전공
        if gradu.rest_credit == None:
            data = {
                'major_info' : major[0], # 전공
                'need_major' : need_major, # 부족학점
                'user_major' : user_major, # 이수한 학점
                'total_credit' : gradu.total_credit, # 졸업 기준 학점
                'major_credit' : gradu.major_credit, # 전공 기준 학점
                'general_essential_credit' : gradu.general_essential_credit, # 교양필수 기준 학점
                'general_selection_credit' : gradu.general_selection_credit, # 교양필수 기준 학점
                'rest_credit' : 0,
                'need_sub_major' : need_sub_major, # 부족 추가전공 학점
                'user_sub_major' : user_sub_major, # 이수한 추가전공 학점
                'sub_major_credit' : gradu.sub_major_credit, # 추가전공 기준 학점
                'sub_major_type' : gradu.sub_major_type,
                'done_major_rest' : done_major_rest[0],
                'done_rest' : done_rest[0]
            },
        else:
            data = {
                'major_info' : major[0], # 전공
                'need_major' : need_major, # 부족학점
                'user_major' : user_major, # 이수한 학점
                'total_credit' : gradu.total_credit, # 졸업 기준 학점
                'major_credit' : gradu.major_credit, # 전공 기준 학점
                'general_essential_credit' : gradu.general_essential_credit, # 교양필수 기준 학점
                'general_selection_credit' : gradu.general_selection_credit, # 교양필수 기준 학점
                'rest_credit' : gradu.rest_credit,
                'need_sub_major' : need_sub_major, # 부족 추가전공 학점
                'user_sub_major' : user_sub_major, # 이수한 추가전공 학점
                'sub_major_credit' : gradu.sub_major_credit, # 추가전공 기준 학점
                'sub_major_type' : gradu.sub_major_type,
                'done_major_rest' : done_major_rest[0],
                'done_rest' : done_rest[0]
            }
    print(data)
    return Response (data)

@api_view(['POST'])
def test_micro_degree(request):
    data = request.data
    student_id = data.get('student_id')
    result = need_micro_degree(student_id)
    if (result == 0) or (result == None) :
        data = {'done_micro_degree' : 0 }
    else:
        data = {'done_micro_degree' : result}
    print(data)
    return Response (data)

