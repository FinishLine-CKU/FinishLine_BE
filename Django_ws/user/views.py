from rest_framework.decorators import api_view
from .scraping import scraping
from rest_framework.response import Response

@api_view(['POST'])
def student_auth(request):
    if request.method == 'POST':
        try:
            data = request.data
            studentId = data.get('studentId')
            studentPW = data.get('studentPW')
            student_id, name, major = scraping(studentId, studentPW)
            print(student_id, name, major)
            data = {'student_id': student_id, 'name' : name, 'major' : major}
        except:
            fault = scraping(studentId, studentPW)
            print(fault)
            data = {'fault' : fault}
    return Response (data)
