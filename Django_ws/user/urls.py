from django.urls import path
from . import views

urlpatterns = [
    path('student_auth/', views.student_auth, name='student_auth'),
    path('register_info/', views.register_info, name='register_info'),
    path('check_register/', views.check_register, name='check_register'),
    path('my_info/', views.my_info, name='my_info')
]