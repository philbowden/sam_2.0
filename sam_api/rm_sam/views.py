from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.forms import (PasswordChangeForm, UserChangeForm,
                                       UserCreationForm)
from django.db.models import F
from django.shortcuts import redirect, render
from django.utils import timezone
from pip._vendor.requests.compat import str
from rest_framework import viewsets

from .forms import SignUpForm, EditProfileForm
from .models import Lesson, Student, Teacher
from .serializers import LessonSerializer, StudentSerializer, TeacherSerializer


class StudentView(viewsets.ModelViewSet):
    # queryset is the model (DB)
    queryset = Student.objects.all()

    # serializer_class is the class that's in serializers.py
    serializer_class = StudentSerializer


class TeacherView(viewsets.ModelViewSet):
    # queryset is the model (DB)
    queryset = Teacher.objects.all()

    # serializer_class is the class that's in serializers.py
    serializer_class = TeacherSerializer


class LessonView(viewsets.ModelViewSet):
    # queryset is the model (DB)
    queryset = Lesson.objects.all()

    # serializer_class is the class that's in serializers.py
    serializer_class = LessonSerializer


@login_required(login_url='/login/')
def admin(request):
    teachers = Teacher.objects.all()
    user_id = request.user.id
    this_teacher = Teacher.objects.get(user_id=user_id)

    return render(request, 'admin.html', {'teachers': teachers, 'this_teacher': this_teacher})


@login_required(login_url='/login/')
def teacher(request, teacher_id):
    date_string = request.session['date_string']
    date_object = datetime.strptime(date_string, '%Y-%m-%d')

    if request.method == "GET":
        change_day = request.GET.get('change_day', None)
        if change_day == 'prev':
            date_object += timedelta(days=-1)
        elif change_day == 'next':
            date_object += timedelta(days=1)

    year_int = date_object.year
    day_int = date_object.day

    month_string = date_object.strftime('%B')
    day_string = date_object.strftime('%A').lower()
    date_string = date_object.strftime('%Y-%m-%d')
    request.session['date_string'] = date_string

    students = Student.objects.all().filter(teacher=teacher_id, day=day_string, active=True).order_by('time')
    current_teacher = Teacher.objects.filter(id=teacher_id)

    if request.method == "POST":
        for student in students:
            request_id = str(student.id) + "_attendance"
            student_attendance = request.POST[request_id]
            if student_attendance == 'true':
                data = 'present'
            else:
                data = "absent"
                if student_attendance == 'excused':
                    data = "makeup"
                    Student.objects.filter(id=student.id).update(make_up=F('make_up') + 1)

            if Lesson.objects.all().filter(student=student.id, teacher=teacher_id, month=month_string,
                                           year=year_int).count() == 0:
                lesson_attrs = {
                    "student_id": student.id,
                    "teacher_id": student.teacher.id,
                    "month": month_string,
                    "year": year_int,
                    "lessons": {
                        day_int: data
                    }
                }
                new_lesson = Lesson.objects.create(**lesson_attrs)
                serializer = LessonSerializer(data=new_lesson)
                if serializer.is_valid():
                    serializer.save()

            else:
                lesson = Lesson.objects.get(student=student.id, teacher=teacher_id, month=month_string, year=year_int)
                lesson.lessons[day_int] = data
                lesson.save()

        return redirect('home')

    else:

        return render(request, 'teacher.html',
                      {'current_teacher': current_teacher, 'students': students,
                       'today': day_string, 'month': month_string, 'day': day_int})


def home(request):
    return render(request, 'home.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            this_teacher = Teacher.objects.get(user_id=user.id)
            request.session['current_id'] = this_teacher.id
            request.session['current_status'] = this_teacher.is_admin
            current_day_object = timezone.localdate()
            date_string = current_day_object.strftime('%Y-%m-%d')
            request.session['date_string'] = date_string

            if this_teacher.is_admin:
                return redirect('/admin_page')
            else:

                return redirect('teacher', teacher_id=this_teacher.id)


        else:
            messages.success(request, ('Error Logging In - Please Try Again...'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/login/')
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)

            status = form.cleaned_data['status']

            is_admin = (status == 'admin')

            teacher_attrs = {
                "is_admin": is_admin,
                "user": user,

            }
            new_teacher = Teacher.objects.create(**teacher_attrs)
            serializer = TeacherSerializer(data=new_teacher)
            if serializer.is_valid():
                serializer.save()

            return redirect('home')

    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'register.html', context)


@login_required(login_url='/login/')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            return redirect('home')

    else:
        form = EditProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'edit_profile.html', context)


@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('home')

    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'change_password.html', context)
