from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.forms import (PasswordChangeForm, UserChangeForm,
                                       UserCreationForm)
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils import timezone
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
    today = timezone.localdate()
    lessons = Lesson.objects.filter(teacher=teacher_id, date__range=["2020-01-01", today], marked=False)
    students = Student.objects.filter(teacher=teacher_id)
    current_teacher = Teacher.objects.filter(id=teacher_id)
    user_id = request.user.id
    this_teacher = Teacher.objects.get(user_id=user_id)
    return render(request, 'teacher.html',
                  {'current_teacher': current_teacher, 'lessons': lessons, 'students': students, 'today': today})


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


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)

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
