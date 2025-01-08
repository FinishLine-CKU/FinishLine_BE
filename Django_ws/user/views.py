from rest_framework.decorators import api_view
from .scraping import scraping
from .models import User
from rest_framework.response import Response

@api_view(['POST'])
def student_auth(request):
    if request.method == 'POST':
        data = request.data
        studentId = data.get('studentId')
        studentPW = data.get('studentPW')
        result = scraping(studentId, studentPW)
        if isinstance(result, tuple):
            student_id, name, major = result
            data = {'student_id': student_id, 'name' : name, 'major' : major}
        else:
            error = result
            data = {'error' : error}
        print(data)
    return Response (data)

@api_view(['POST'])
def register_info(request):
    if request.method == 'POST':
        data = request.data
        name = data.get('name')
        major = data.get('major')
        student_id = data.get('student_id')
        additionalMajorType = data.get('additionalMajorType')
        additionalMajor = data.get('additionalMajor')
        microDegree = data.get('microDegree')
        password = data.get('password')
        print(data)
    return Response (data)