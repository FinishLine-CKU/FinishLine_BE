from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from io import BytesIO
from .extract import extract_from_pdf_table
from .extract import save_pdf_data_to_db
import logging

logger = logging.getLogger(__name__)

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

                extracted_table = extract_from_pdf_table(pdf_bytes)

                saved_subjects = save_pdf_data_to_db(extracted_table)

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
