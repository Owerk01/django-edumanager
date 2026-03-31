from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('journal/', JournalView.as_view(), name='journal'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('students/', StudentsView.as_view(), name='students_list'),
    path('students/add/', StudentAddView.as_view(), name='student_add'),
    path('students/<slug:slug>/', StudentView.as_view(), name='student_detail'),
    path('students/<slug:slug>/edit/', StudentEditView.as_view(), name='student_edit'),
    path('students/<slug:slug>/delete/', StudentDeleteView.as_view(), name='student_delete'),
    path('teachers/<slug:slug>/delete/', TeacherDeleteView.as_view(), name='teacher_delete'),
    path('teachers/', TeachersView.as_view(), name='teachers_list'),
    path('teachers/add/', TeacherAddView.as_view(), name='teacher_add'),
    path('teachers/<slug:slug>/', TeacherView.as_view(), name='teacher_detail'),
    path('teachers/<slug:slug>/edit/', TeacherEditView.as_view(), name='teacher_edit'),
    path('courses/add/', CourseAddView.as_view(), name='course_add'),
    path('courses/<slug:slug>/', CourseView.as_view(), name='course_detail'),
    path('courses/<slug:slug>/edit/', CourseEditView.as_view(), name='course_edit'),
    path('courses/<slug:slug>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('courses/', CoursesView.as_view(), name='courses_list'),
    path('grades/add/', GradeAddView.as_view(), name='grade_add'),
    path('grades/<slug:slug>/edit/', GradeEditView.as_view(), name='grade_edit'),
    path('grades/<slug:slug>/delete/', GradeDeleteView.as_view(), name='grade_delete'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('reg/', RegisterUser.as_view(), name='reg')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)