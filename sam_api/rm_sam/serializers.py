from rest_framework import serializers
from .models import Teacher, Student, Lesson


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'first', 'last', 'user', 'is_admin')


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'first', 'last', 'email', 'phone', 'time', 'day', 'start_date', 'instrument',
                  'teacher', 'charge_rate', 'notes', 'parent_first', 'parent_last', 'birthdate', 'present',
                  'unexcused', 'make_up', 'active', 'creator', 'created')


class LessonSerializer(serializers.ModelSerializer):
    lessons = serializers.JSONField()

    class Meta:
        model = Lesson
        fields = ('id','student', 'teacher', 'month', 'year', 'lessons')
