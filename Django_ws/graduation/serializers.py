from rest_framework import serializers
from .models import MyDoneLecture

class MyDoneLectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyDoneLecture
        fields = ['year', 'semester', 'lecture_type', 'lecture_topic', 'lecture_name', 'credit', 'grade']