from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20)
    student_id = models.CharField(max_length=10, unique=True, primary_key=True)
    password = models.CharField(max_length=20)
    major = models.CharField(max_length=40)
    sub_major_type = models.CharField(max_length=5, blank=True, null=True)
    sub_major = models.CharField(max_length=40, blank=True, null=True)
    micro_degree = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name



