from django.db import models

class MyDoneLecture(models.Model):
    year = models.CharField(max_length=5)
    semester = models.CharField(max_length=5)
    lecture_type = models.CharField(max_length=50)
    lecture_topic = models.CharField(max_length=200, blank=True, null=True)
    lecture_name = models.CharField(max_length=200)
    credit = models.DecimalField(max_digits=3, decimal_places=1)
    grade = models.CharField(max_length=5)
    
    def __str__(self):
        return f"{self.subject_name} ({self.year}-{self.semester} {self.lecture_type})"
