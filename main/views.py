from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Teacher, Course, Grade
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout, login
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden, HttpResponseNotFound

from .models import Student, Course, Grade, InvitationCode
from .forms import CourseAddForm, RegisterUserForm, StudentAddForm, TeacherAddForm, GradeAddForm, GradeEditForm, CourseFilterForm, StudentFilterForm, TeacherFilterForm, GradeFilterForm, ProfileEditForm
from django.utils import timezone
# Create your views here.

def handler_403(request, exception):
    return HttpResponseForbidden("Доступ запрещён. Недостаточно прав.")

def index(r):
    context = {
        'students_count': Student.objects.count(),
        'teachers_count': Teacher.objects.count(),
        'courses_count': Course.objects.count(),
        'grades_count': Grade.objects.count(),
        'recent_courses': Course.objects.all()[:5] if r.user.is_authenticated else None
    }

    return render(r, 'main/index.html', context)

class StudentsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Student
    template_name = 'main/students_list.html'
    context_object_name = 'students'
    paginate_by = 10
    paginate_orphans = 3
    login_url = '/login/'
    permission_required = 'main.view_student'

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get('query', '').strip()
        age_min = self.request.GET.get('age_min')
        age_max = self.request.GET.get('age_max')
        gender = self.request.GET.get('gender')
        course_id = self.request.GET.get('course')

        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(surname__icontains=query))

        if age_min:
            queryset = queryset.filter(age__gte=age_min)
        if age_max:
            queryset = queryset.filter(age__lte=age_max)

        if gender:
            queryset = queryset.filter(gender=gender)

        if course_id:
            queryset = queryset.filter(courses__id=course_id)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = StudentFilterForm(self.request.GET)
        context['courses_list'] = Course.objects.all()
        return context
    
class StudentView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Student
    template_name = 'main/student_detail.html'
    context_object_name = 'student'
    slug_url_kwarg = 'slug'
    login_url = '/login/'
    permission_required = 'main.view_student'

class StudentAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = StudentAddForm
    template_name = 'main/student_add.html'
    success_url = reverse_lazy('students_list')
    login_url = '/login/'
    permission_required = 'main.add_student'

class StudentEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Student
    form_class = StudentAddForm
    template_name = 'main/student_edit.html'
    success_url = reverse_lazy('students_list')
    slug_url_kwarg = 'slug'
    login_url = '/login/'
    permission_required = 'main.change_student'

class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Student
    template_name = ('main/student_del_confirm.html')
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('students_list')
    login_url = '/login/'
    permission_required = 'main.delete_student'

class TeachersView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Teacher
    template_name = 'main/teachers_list.html'
    context_object_name = 'teachers'
    paginate_by = 10
    paginate_orphans = 3
    login_url = '/login/'
    permission_required = 'main.view_teacher'

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get('query', '').strip()
        age_min = self.request.GET.get('age_min')
        age_max = self.request.GET.get('age_max')
        gender = self.request.GET.get('gender')
        course_id = self.request.GET.get('course')

        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(surname__icontains=query))

        if age_min:
            queryset = queryset.filter(age__gte=age_min)
        if age_max:
            queryset = queryset.filter(age__lte=age_max)

        if gender:
            queryset = queryset.filter(gender=gender)

        if course_id:
            queryset = queryset.filter(courses__id=course_id)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = TeacherFilterForm(self.request.GET)
        context['courses_list'] = Course.objects.all()
        return context
    
class TeacherView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Teacher
    template_name = 'main/teacher_detail.html'
    context_object_name = 'teacher'
    slug_url_kwarg = 'slug'
    login_url = '/login/'
    permission_required = 'main.view_teacher'

class TeacherAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = TeacherAddForm
    template_name = 'main/teacher_add.html'
    success_url = reverse_lazy('teachers_list')
    login_url = '/login/'
    permission_required = 'main.add_teacher'

class TeacherEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherAddForm
    template_name = 'main/teacher_edit.html'
    success_url = reverse_lazy('teachers_list')
    slug_url_kwarg = 'slug'
    login_url = '/login/'
    permission_required = 'main.change_teacher'

class TeacherDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Teacher
    template_name = ('main/teacher_del_confirm.html')
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('teachers_list')
    login_url = '/login/'
    permission_required = 'main.delete_teacher'

class CoursesView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Course
    template_name = 'main/courses_list.html'
    context_object_name = 'courses'
    paginate_by = 10
    paginate_orphans = 3
    login_url = '/login/'
    permission_required = 'main.view_course'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        form = CourseFilterForm(self.request.GET)

        if form.is_valid(): 
            
            lang = form.cleaned_data.get('lang')
            if lang:
                queryset = queryset.filter(name=lang) 
            
            course_num = form.cleaned_data.get('num')
            if course_num:
                queryset = queryset.filter(course_num=course_num)

            start_from = form.cleaned_data.get('start_date_from')
            if start_from:
                queryset = queryset.filter(start_date__gte=start_from)
            
            start_to = form.cleaned_data.get('start_date_to')
            if start_to:
                queryset = queryset.filter(start_date__lte=start_to)
            
            end_from = form.cleaned_data.get('end_date_from')
            if end_from:
                queryset = queryset.filter(end_date__gte=end_from)
            
            end_to = form.cleaned_data.get('end_date_to')
            if end_to:
                queryset = queryset.filter(end_date__lte=end_to) 

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = CourseFilterForm(self.request.GET)
        return context

class CourseView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Course
    template_name = 'main/course_detail.html'
    context_object_name = 'course'
    slug_url_kwarg = 'slug'
    login_url = '/login/'
    permission_required = 'main.view_course'

class CourseAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = CourseAddForm
    template_name = 'main/course_add.html'
    success_url = reverse_lazy('courses_list')
    login_url = '/login/'
    permission_required = 'main.add_course'

class CourseEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Course
    form_class = CourseAddForm
    template_name = 'main/course_edit.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('courses_list')
    login_url = '/login/'
    permission_required = 'main.change_course'

class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Course
    template_name = 'main/course_del_confirm.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('courses_list')
    login_url = '/login/'
    permission_required = 'main.delete_course'

class GradeAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = GradeAddForm
    template_name = 'main/grade_add.html'
    success_url = reverse_lazy('journal')
    login_url = '/login/'
    permission_required = 'main.add_grade'

class GradeEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Grade
    form_class = GradeEditForm
    template_name = 'main/grade_edit.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('journal')
    login_url = '/login/'
    permission_required = 'main.change_grade'

class GradeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Grade
    template_name = 'main/grade_del_confirm.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('journal')
    login_url = '/login/'
    permission_required = 'main.delete_grade'

class JournalView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Grade
    template_name = 'main/journal.html'
    context_object_name = 'grades'
    paginate_by = 10
    paginate_orphans = 3
    login_url = '/login/'
    permission_required = 'main.view_grade'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = GradeFilterForm(self.request.GET)

        if form.is_valid():
            student = form.cleaned_data.get('student')
            if student:
                queryset = queryset.filter(student=student)
            
            course = form.cleaned_data.get('course')
            if course:
                queryset = queryset.filter(course=course)

            grade_min = form.cleaned_data.get('grade_min')
            if grade_min:
                queryset = queryset.filter(grade__gte=grade_min)
            
            grade_max = form.cleaned_data.get('grade_max')
            if grade_max:
                queryset = queryset.filter(grade__lte=grade_max)

            date_from = form.cleaned_data.get('date_from')
            if date_from:
                queryset = queryset.filter(date__gte=date_from)
            
            date_to = form.cleaned_data.get('date_to')
            if date_to:
                queryset = queryset.filter(date__lte=date_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = GradeFilterForm(self.request.GET)
        context['students_list'] = Student.objects.all()
        context['courses_list'] = Course.objects.all()
        return context
    
class ProfileView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = 'main/profile.html'
    context_object_name = 'grades'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if hasattr(user, 'student_profile') and user.student_profile is not None:
            context['profile'] = user.student_profile
            context['profile_type'] = 'student'
            context['grades'] = Grade.objects.filter(student=user.student_profile).select_related('course')
        elif hasattr(user, 'teacher_profile') and user.teacher_profile is not None:
            context['profile'] = user.teacher_profile
            context['profile_type'] = 'teacher'
            context['grades'] = None
        else:
            context['profile'] = None
            context['profile_type'] = 'other'
            context['grades'] = None
        
        context['user'] = user  
        return context

class ProfileEditView(LoginRequiredMixin, FormView):
    form_class = ProfileEditForm
    template_name = 'main/profile_edit.html'
    success_url = reverse_lazy('profile')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if hasattr(user, 'student_profile'):
            context['profile_type'] = 'student'
            context['profile'] = user.student_profile
        elif hasattr(user, 'teacher_profile'):
            context['profile_type'] = 'teacher'
            context['profile'] = user.teacher_profile
        else:
            context['profile_type'] = 'admin'
            context['profile'] = None
    
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['username'] = user.username
        initial['email'] = user.email

        profile = self.get_profile()
        if profile and hasattr(profile, 'photo'):
            initial['photo'] = profile.photo
        
        return initial
    
    def get_profile(self):
        user = self.request.user
        if hasattr(user, 'student_profile'):
            return user.student_profile
        elif hasattr(user, 'teacher_profile'):
            return user.teacher_profile
        return None
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        photo = form.cleaned_data.get('photo')

        user = self.request.user
        
        if username and username != user.username:
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Этот логин уже занят')
                return self.form_invalid(form)
            user.username = username
        
        if email:
            user.email = email
        
        user.save()
        
        profile = self.get_profile()
        if profile and photo:
            profile.photo = photo
            profile.save()
        
        return super().form_valid(form)

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'main/login.html'
    def get_success_url(self) -> str:
        return reverse_lazy('index')
    
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/reg.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()

        code = form.cleaned_data.get('code')
        inv_code = InvitationCode.objects.get(code=code)
        group = inv_code.group
        user.groups.add(group)

        profile = inv_code.get_profile()
        if profile:
            profile.user = user
            profile.save()

        inv_code.is_used = True
        inv_code.used_at = timezone.now()
        inv_code.save()
        login(self.request, user)
        return redirect('index')
    
def logout_user(r):
    logout(r)
    return redirect('index')    

def handler_403(request, exception):
    return render(request, 'main/403.html', status=403)

def handler_404(request, exception):
    return render(request, 'main/404.html', status=404)

def handler_500(request, exception):
    return render(request, 'main/500.html', status=500)