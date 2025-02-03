from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.response import Response
from io import BytesIO
from .extract import extract_from_pdf_table
from .extract import save_pdf_data_to_db
from .extract import extract_major_from_pdf_table
import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import MyDoneLecture
from .models import AllLectureData
from .models import NowLectureData
from .serializers import MyDoneLectureSerializer
from .serializers import AllLectureDataSerializer
from .serializers import NowLectureDataSerializer

logger = logging.getLogger(__name__)

class MyDoneLectureModelViewSet(ModelViewSet):
    queryset = MyDoneLecture.objects.all()
    serializer_class = MyDoneLectureSerializer
    
    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return super().create(request, *args, **kwargs)

class AllLectureDataModelViewSet(ModelViewSet):
    queryset = AllLectureData.objects.all()
    serializer_class = AllLectureDataSerializer
    
class NowLectureModelViewSet(ModelViewSet):
    queryset = NowLectureData.objects.all()
    serializer_class = NowLectureDataSerializer

    @action(detail=False, methods=['get'], url_path='filter-by-code/(?P<lectureCode>[^/.]+)')
    def filter_by_code(self, request, lectureCode=None): 
        queryset = NowLectureData.objects.filter(lecture_code=lectureCode)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def upload_pdf(request):
    if 'files' not in request.FILES:
        return Response({'error': 'No file uploaded'}, status=400)

    files = request.FILES.getlist('files')
    result_data = []
    duplicate_files = []

    for uploaded_file in files:
        if uploaded_file.name.endswith('.pdf'):
            try:
                pdf_bytes = BytesIO(uploaded_file.read())

                extracted_major = extract_major_from_pdf_table(pdf_bytes)

                extracted_table = extract_from_pdf_table(pdf_bytes)

                saved_subjects = save_pdf_data_to_db(extracted_table, extracted_major)

                if saved_subjects: 
                    result_data.append({
                        'file': uploaded_file.name,
                        'status': 'saved',
                        'message': f"File '{uploaded_file.name}' uploaded successfully."
                    })
                else:
                    duplicate_files.append(uploaded_file.name)

            except Exception as e:
                logger.error(f"Error processing file {uploaded_file.name}: {str(e)}")
                return Response({'error': f'Error processing file {uploaded_file.name}: {str(e)}'}, status=500)
    logger.info("File processing completed.")
    return Response({
        'message': 'Files processed successfully',
        'data': result_data,
        'duplicate_files': duplicate_files,
    })