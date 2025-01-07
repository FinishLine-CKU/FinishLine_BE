from django.urls import path
from . import views

urlpatterns = [
    path('student_auth/', views.student_auth, name='student_auth'),
]