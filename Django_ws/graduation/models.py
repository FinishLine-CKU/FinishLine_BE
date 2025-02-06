from django.db import models
from django.db.models.fields.related import ForeignKey

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
    user_id = models.CharField(max_length=30, null=False)
    
    alllecture = models.ForeignKey(AllLectureData, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.lecture_name} ({self.year}-{self.semester} {self.lecture_type})"

class Standard(models.Model):
    index = models.AutoField(primary_key=True)
    college = models.CharField(max_length=50)
    year = models.CharField(max_length=30)
    total_credit = models.DecimalField(max_digits=5, decimal_places=1)
    sub_major_type = models.CharField(max_length=30, blank=True, null=True)
    sub_major_credit = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    major_credit = models.DecimalField(max_digits=4, decimal_places=1)
    general_essential_credit = models.DecimalField(max_digits=4, decimal_places=1)
    general_selection_credit = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    rest_credit = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    micro_degree_credit = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    
    def __str__(self):
        return self.college