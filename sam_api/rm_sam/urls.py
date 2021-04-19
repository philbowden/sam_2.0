from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('rm_sam', views.StudentView)
router.register('teacher_api', views.TeacherView)
router.register('lesson_api', views.LessonView)

urlpatterns = [
    path('', views.home, name="home"),
    path('sam_api/', include(router.urls)),
    path('admin_page', views.admin, name='admin'),
    path('teacher/<int:teacher_id>/', views.teacher, name='teacher'),
    path('teacher/<int:teacher_id>/<int:change_day>/<direction>', views.teacher, name='teacher'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password', views.change_password, name='change_password'),
]
