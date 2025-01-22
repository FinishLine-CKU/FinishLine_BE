from rest_framework import serializers
from .models import MyDoneLecture
from .models import AllLectureData

class MyDoneLectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyDoneLecture
        fields = ['year', 'semester', 'lecture_code', 'lecture_type', 'lecture_topic', 'lecture_name', 'credit', 'grade']

class AllLectureDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllLectureData
        fields = ['year', 'semester', 'lecture_code', 'lecture_name', 'lecture_type', 'lecture_topic', 'credit']