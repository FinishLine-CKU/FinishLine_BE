from rest_framework.decorators import api_view
from .scraping import scraping
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
