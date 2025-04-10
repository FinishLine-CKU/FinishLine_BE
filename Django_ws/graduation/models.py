from django.db import models
from django.db.models.fields.related import ForeignKey

#전체 과목 데이터
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
    
#현재 과목 데이터(25년도)
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
    
#내 기이수 과목 데이터
class MyDoneLecture(models.Model):
    mydone_id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=5)
    semester = models.CharField(max_length=5)
    lecture_type = models.CharField(max_length=50)
    lecture_topic = models.CharField(max_length=200, blank=True, null=True)
    lecture_code = models.CharField(max_length=50, null=True, blank=True)
    lecture_name = models.CharField(max_length=200)
    credit = models.DecimalField(max_digits=3, decimal_places=1)
    user_id = models.CharField(max_length=30, null=True)
    can_delete = models.BooleanField(default=False)

    alllecture = models.ForeignKey(AllLectureData, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.lecture_name} ({self.lecture_topic}) ({self.credit})"
    
#교양 요건 연도별 기준표
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

    def __str__(self):
        return f"{self.lecture_name} ({self.year}-{self.semester} {self.lecture_type})"

class Standard(models.Model):
    index = models.AutoField(primary_key=True)
    college = models.CharField(max_length=50)
    year = models.CharField(max_length=30)
    total_standard = models.DecimalField(max_digits=5, decimal_places=1)
    sub_major_type = models.CharField(max_length=30, blank=True, null=True)
    sub_major_credit = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    major_standard = models.DecimalField(max_digits=4, decimal_places=1)
    essential_GE_standatd = models.DecimalField(max_digits=4, decimal_places=1)
    general_selection_credit = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    rest_credit = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    micro_degree_credit = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    
    def __str__(self):
        return self.college
