from rest_framework import serializers
from .models import MyDoneLecture
from .models import AllLectureData
from .models import NowLectureData

class MyDoneLectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyDoneLecture
        fields = ['year', 'semester', 'lecture_code', 'lecture_type', 'lecture_topic', 'lecture_name', 'credit']

class AllLectureDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllLectureData
        fields = ['year', 'semester', 'lecture_code', 'lecture_name', 'lecture_type', 'lecture_topic', 'credit']

class NowLectureDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NowLectureData
        fields = ['year', 'semester', 'lecture_code', 'lecture_name', 'lecture_type', 'lecture_topic', 'credit']