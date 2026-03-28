from django import forms
from .models import Course, Student, Grade, Teacher, InvitationCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
    
class CourseAddForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size':'10', 'class': 'form-control'}),
        label="Студенты курса"
    )

    teachers= forms.ModelMultipleChoiceField(
        queryset=Teacher.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size':'10', 'class': 'form-control'}),
        label="Преподаватели курса"
    )

    class Meta:
        model = Course
        fields = ('name', 'course_num', 'students', 'teachers', 'start_date', 'end_date', 'description')

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'data123'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'data123'})
        }

class CourseFilterForm(forms.Form):
    lang = forms.ChoiceField(required=False, label='Язык программирования', choices=[('', 'Всё')] + Course.langs)
    num = forms.IntegerField(required=False, label='Номер курса', min_value=1, max_value=100)
    start_date_from = forms.DateField(required=False, label='Начало до', widget=forms.DateInput(attrs={'type':'date'}))
    start_date_to = forms.DateField(required=False, label='Начало после', widget=forms.DateInput(attrs={'type':'date'}))
    end_date_from = forms.DateField(required=False, label='Окончание до', widget=forms.DateInput(attrs={'type':'date'}))
    end_date_to = forms.DateField(required=False, label='Окончание после', widget=forms.DateInput(attrs={'type':'date'}))
    
class StudentAddForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('surname', 'name', 'second_name', 'age', 'gender', 'courses', 'photo')
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'accept':'image/*'})
        }

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age is None:
            return age
            
        if age < 18: 
            raise ValidationError('Возраст не подходит')
            
        if age > 99:
            raise ValidationError('Столько не живут!')
        
        return age
    
class ProfileEditForm(forms.Form):
    username = forms.CharField(
        label='Логин', 
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email', 
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    photo = forms.ImageField(
        label='Фото', 
        required=False, 
        widget=forms.ClearableFileInput(attrs={
            'accept': 'image/*', 
            'class': 'form-control'
        })
    )
    
class StudentFilterForm(forms.Form):
    query = forms.CharField(required=False, label='Поиск по имени/фамилии')
    age_min = forms.IntegerField(required=False, label='Минимальный возраст', min_value=18, max_value=100)
    age_max = forms.IntegerField(required=False, label='Максимальный возраст', min_value=18, max_value=100)
    gender = forms.ChoiceField(required=False, label='Пол', choices=[('', 'Все'), ('m', 'Мужской'), ('f', 'Женский')])
    course = forms.ModelChoiceField(required=False, label='Курс', queryset=Course.objects.all(), empty_label='Все курсы')
    
class TeacherAddForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('name', 'surname', 'second_name', 'age', 'gender', 'courses', 'photo')
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'accept':'image/*'})
        }

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age is None:
            return age
            
        if age < 18: 
            raise ValidationError('Возраст не подходит')
            
        if age > 99:
            raise ValidationError('Возраст не подходит')
        
        return age
    
class TeacherFilterForm(forms.Form):
    query = forms.CharField(required=False, label='Поиск по имени/фамилии')
    age_min = forms.IntegerField(required=False, label='Минимальный возраст', min_value=18, max_value=100)
    age_max = forms.IntegerField(required=False, label='Максимальный возраст', min_value=18, max_value=100)
    gender = forms.ChoiceField(required=False, label='Пол', choices=[('', 'Все'), ('m', 'Мужской'), ('f', 'Женский')])
    course = forms.ModelChoiceField(required=False, label='Курс', queryset=Course.objects.all(), empty_label='Все курсы')

class GradeAddForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('grade', 'student', 'course', 'date')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class GradeEditForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["grade", "date"]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class GradeFilterForm(forms.Form):
    grade_min = forms.IntegerField(required=False, label='Минимальная оценка', min_value=1, max_value=10)
    grade_max = forms.IntegerField(required=False, label='Максимальная оценка', min_value=1, max_value=10)
    course = forms.ModelChoiceField(required=False, label='Курсы', queryset=Course.objects.all(), empty_label='Все курсы')
    student = forms.ModelChoiceField(required=False, label='Студенты', queryset=Student.objects.all(), empty_label='Все Студенты')
    date_from = forms.DateField(required=False, label='Поставлена после', widget=forms.DateInput(attrs={'type':'date'}))
    date_to = forms.DateField(required=False, label='Поставлена до', widget=forms.DateInput(attrs={'type':'date'}))
        
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    code = forms.CharField(label='Пригласительный код', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите код'}), max_length=32)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'code')

    def clean_code(self):
        code = self.cleaned_data.get('code')

        if not code:
            raise forms.ValidationError("Введите пригласительный код")
        
        try:
            inv_code = InvitationCode.objects.get(code=code)
            if not inv_code.is_valid():
                if inv_code.is_used:
                    raise forms.ValidationError("Пригласительный код уже использован")
                else:
                    raise forms.ValidationError("Срок действия пригласительного кода истёк")
        except InvitationCode.DoesNotExist:
            raise forms.ValidationError("Неверный пригласительный код")
        
        return code