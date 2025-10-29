from django.db import models

# Create your models here.
class User(models.Model):
    last_login = models.DateTimeField(null=True)
    date_time_joined = models.DateTimeField()
    name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=30, unique=True, primary_key=True)
    password = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    sub_major_type = models.CharField(max_length=30, blank=True, null=True)
    sub_major = models.CharField(max_length=100, blank=True, null=True)
    MD = models.CharField(max_length=100, blank=True, null=True)
    lack_major = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    lack_GE = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    lack_sub_major = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    lack_MD = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    lack_education = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    lack_rest = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    done_major = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    done_GE = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    done_GE_rest = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    done_major_rest = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    done_rest = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    done_sub_major = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    done_sub_major_rest = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    done_MD = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    done_MD_rest = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    done_education_rest = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class VisitorCount(models.Model):
    id = models.IntegerField(default=1, primary_key=True)
    total_visitor = models.IntegerField(default=0, blank=True, null=True)
    today_visitor = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.today_visitor

class MajorMap(models.Model):
    college = models.CharField(max_length=100, blank=True, null=True)
    major_label = models.CharField(max_length=100, unique=True)
    major_code = models.CharField(max_length=100, unique=True, primary_key=True)
    major_type = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.major_label

class MajorAlias(models.Model):
    major_code = models.CharField(max_length=100)
    alias = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return self.alias