from django.urls import path, include
from . import views

urlpatterns = [
    path('upload_pdf/', views.upload_pdf),
]