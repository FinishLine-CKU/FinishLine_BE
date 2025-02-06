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
    user_id = models.CharField(max_length=30, null=True)

    alllecture = models.ForeignKey(AllLectureData, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.lecture_name} ({self.lecture_topic}) ({self.credit})"
    
class liberRequire(models.Model):
    liber_id = models.AutoField(primary_key=True)
    연도 = models.CharField(max_length=5, blank=True, null=True)
    인간학 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    봉사활동 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    VERUM캠프 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    논리적사고와글쓰기= models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    창의적사고와코딩 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    외국어 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    고전탐구 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    사유와지혜 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    가치와실천 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    상상력과표현 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    인문융합 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    균형1 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    균형2 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    균형3 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    균형4 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    MSC교과군 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    계열기초 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    철학적인간학 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
    신학적인간학 = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1) 
