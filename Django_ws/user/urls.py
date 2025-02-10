from django.urls import path
from . import views

urlpatterns = [
    path('student_auth/', views.student_auth, name='student_auth'),
    path('register_info/', views.register_info, name='register_info'),
    path('check_register/', views.check_register, name='check_register'),
    path('my_info/', views.my_info, name='my_info'),
    path('remove_membership/', views.remove_membership, name='remove_membership'),
    path('change_pw/', views.change_pw, name='change_pw'),
    path('change_info/', views.change_info, name='change_info'),
    path('lack_credit/', views.lack_credit, name='lack_credit')
]