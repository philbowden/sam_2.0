import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

NULL_AND_BLANK = {'null': True, 'blank': True}


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)


class Student(models.Model):
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(max_length=10)
    time = models.CharField(max_length=30)
    day = models.CharField(max_length=100)
    start_date = models.DateField(auto_now_add=False, auto_now=False, default=datetime.date.today)
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    instrument = models.CharField(max_length=100, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    charge_rate = models.CharField(max_length=30, default='2020 rate')
    notes = models.TextField(blank=True, null=True)
    parent_first = models.CharField(max_length=100, null=True)
    parent_last = models.CharField(max_length=100, null=True)
    birthdate = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    present = models.IntegerField(default=0)
    unexcused = models.IntegerField(default=0)
    make_up = models.IntegerField(default=0)
    vacay_start_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    vacay_end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, **NULL_AND_BLANK, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.first + ' ' + self.last


class Lesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False, default=datetime.date.today)
    present = models.BooleanField(default=False)
    marked = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    creator = models.ForeignKey(User, **NULL_AND_BLANK, on_delete=models.CASCADE)

    def is_past_due(self):
        return timezone.localdate() > self.date

    def is_today(self):
        # today = datetime.datetime.utcnow().date()
        # yesterday = today - datetime.timedelta(days=1)
        # today = yesterday
        # return datetime.date.today() == self.date
        return timezone.localdate() == self.date
