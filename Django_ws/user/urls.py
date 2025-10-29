from django.urls import path
from . import views

urlpatterns = [
    path('student_auth/', views.student_auth, name='student_auth'),
    path('register_info/', views.register_info, name='register_info'),
    path('major_mapping/', views.major_mapping, name='major_mapping'),
    path('check_register/', views.check_register, name='check_register'),
    path('reset_check_register/', views.reset_check_register, name='reset_check_register'),
    path('my_info/', views.my_info, name='my_info'),
    path('remove_membership/', views.remove_membership, name='remove_membership'),
    path('change_pw/', views.change_pw, name='change_pw'),
    path('change_info/', views.change_info, name='change_info'),
    path('lack_credit/', views.lack_credit, name='lack_credit'),
    path('set_visitor_cookie/', views.set_visitor_cookie, name='set_visitor_cookie'),
    path('get_visitor_info/', views.get_visitor_info, name='get_visitor_info'),
]