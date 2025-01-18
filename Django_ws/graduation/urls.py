from django.urls import path
from . import views

urlpatterns = [
    path('upload_pdf/', views.upload_pdf),
]