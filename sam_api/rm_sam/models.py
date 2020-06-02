import datetime
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from jsonfield import JSONField


class Teacher(models.Model):
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.first + ' ' + self.last


class Student(models.Model):
    first = models.CharField(max_length=100, default=None)
    last = models.CharField(max_length=100, default=None)
    # email = models.EmailField(max_length=100, null=True, blank=True)
    # phone = models.CharField(max_length=10, null=True, blank=True)
    time = models.CharField(max_length=30, null=True, blank=True)
    day = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(auto_now_add=False, auto_now=False, default=datetime.date.today, null=True,
                                  blank=True)
    # instrument = models.CharField(max_length=100, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    charge_rate = models.CharField(max_length=30, default='$120', null=True)
    notes = models.TextField(blank=True, null=True)
    # parent_first = models.CharField(max_length=100, null=True)
    # parent_last = models.CharField(max_length=100, null=True)
    # birthdate = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    present = models.IntegerField(default=0)
    unexcused = models.IntegerField(default=0)
    make_up = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.first + ' ' + self.last

    def __get_time__(self):
        date = parse_date(self.time)
        return date


class Lesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    month = models.CharField(max_length=9, default=timezone.now().strftime('%B'))
    year = models.IntegerField(default=timezone.now().year)
    lessons = JSONField(null=True, blank=True)