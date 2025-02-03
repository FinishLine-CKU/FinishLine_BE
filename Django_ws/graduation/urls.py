from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
# from .views import MyDoneLectureViewSet
from .views import MyDoneLectureModelViewSet
from .views import AllLectureDataModelViewSet
from .views import NowLectureModelViewSet

router = DefaultRouter()
router.register(r'mydonelecture', MyDoneLectureModelViewSet)
router.register(r'allLectureData', AllLectureDataModelViewSet)
router.register(r'nowLectureData', NowLectureModelViewSet)

urlpatterns = [
    path('upload_pdf/', views.upload_pdf),
    path('api/', include(router.urls)),
]