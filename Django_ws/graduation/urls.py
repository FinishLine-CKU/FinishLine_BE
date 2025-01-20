from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import MyDoneLectureViewSet

router = DefaultRouter()
router.register(r'mydonelecture', MyDoneLectureViewSet)

urlpatterns = [
    path('upload_pdf/', views.upload_pdf),
    path('api/', include(router.urls)),
]