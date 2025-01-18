from rest_framework.decorators import api_view
from rest_framework.response import Response
from io import BytesIO
from .extract import extract_from_pdf_table

@api_view(['POST'])
def upload_pdf(request):
    if 'files' not in request.FILES:
        return Response({'error': 'No file uploaded'}, status=400)
    
    files = request.FILES.getlist('files') 
    uploaded_files = []

    for uploaded_file in files:
        if uploaded_file.name.endswith('.pdf'):
            try:
                
                pdf_bytes = BytesIO(uploaded_file.read())
                
                extracted_table = extract_from_pdf_table(pdf_bytes)

                uploaded_files.append({
                    'file_name': uploaded_file.name,
                    'data': extracted_table,
                })
            except Exception as e:
                return Response({'error': f'Error processing file {uploaded_file.name}: {str(e)}'}, status=500)
            
    print("Extracted Table Data:", extracted_table)

    return Response({'message': 'Files processed successfully', 'files': uploaded_files})
