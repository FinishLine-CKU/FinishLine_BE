from django.db import models
from django.contrib.auth.models import User

class AllLectureData(models.Model):
    alllecture_id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=5)
    semester = models.CharField(max_length=5)
    lecture_code = models.CharField(max_length=50)
    lecture_name = models.CharField(max_length=100)
    lecture_type = models.CharField(max_length=50)
    lecture_topic = models.CharField(max_length=200, blank=True, null=True)
    credit = models.DecimalField(max_digits=3, decimal_places=1)
    major_code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.lecture_name} ({self.year}-{self.semester})"
    
class NowLectureData(models.Model):
    nowlecture_id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=5)
    semester = models.CharField(max_length=5)
    lecture_code = models.CharField(max_length=50)
    lecture_name = models.CharField(max_length=100)
    lecture_type = models.CharField(max_length=50)
    lecture_topic = models.CharField(max_length=200, blank=True, null=True)
    credit = models.DecimalField(max_digits=3, decimal_places=1)
    major_code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.lecture_name} ({self.year}-{self.semester})"
    

class MyDoneLecture(models.Model):
    mydone_id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=5)
    semester = models.CharField(max_length=5)
    lecture_type = models.CharField(max_length=50)
    lecture_topic = models.CharField(max_length=200, blank=True, null=True)
    lecture_code = models.CharField(max_length=50, null=True, blank=True)
    lecture_name = models.CharField(max_length=200)
    credit = models.DecimalField(max_digits=3, decimal_places=1)
    grade = models.CharField(max_length=5, blank=True, null=True)
    
    alllecture = models.ForeignKey(AllLectureData, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.lecture_name} ({self.year}-{self.semester} {self.lecture_type})"
