from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=30, unique=True, primary_key=True)
    password = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    sub_major_type = models.CharField(max_length=30, blank=True, null=True)
    sub_major = models.CharField(max_length=100, blank=True, null=True)
    micro_degree = models.CharField(max_length=100, blank=True, null=True)
    need_major = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    need_general = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    need_sub_major = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    need_rest = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    done_major = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    done_general = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    done_rest = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    done_major_rest = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    done_sub_major = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return self.name



