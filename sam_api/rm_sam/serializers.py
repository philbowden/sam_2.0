from rest_framework import serializers
from .models import Teacher, Student, Lesson


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'user', 'admin')


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'first', 'last', 'phone', 'email', 'time', 'day', 'start_date', 'end_date', 'instrument',
                  'teacher', 'charge_rate', 'notes', 'parent_first', 'parent_last', 'birthdate', 'present',
                  'unexcused', 'make_up', 'vacay_start_date', 'vacay_end_date', 'active')


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'student', 'teacher', 'date', 'present', 'marked', 'created')
