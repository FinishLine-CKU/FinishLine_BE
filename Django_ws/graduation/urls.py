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
    path('general_check/', views.general_check),
    path('api/', include(router.urls)),
    path('api/mydonelecture/<int:pk>/', MyDoneLectureModelViewSet.as_view({'delete': 'destroy'}), name='delete_my_done_lecture'),
    path('test_major/', views.test_major, name='test_major'),
    path('test_micro_degree/', views.test_micro_degree, name='test_micro_degree'),
    path('oneclick_test/', views.oneclick_test),
]