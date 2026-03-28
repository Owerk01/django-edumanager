from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse
from pytils.translit import slugify as ruslugify
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from datetime import timedelta
import secrets
from django.utils import timezone
import string

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=20,
                            verbose_name='Имя',
                            null=False,
                            blank=False)
    
    surname = models.CharField(max_length=20,
                               verbose_name='Фамилия',
                               null=False,
                               blank=False)
    
    second_name = models.CharField(max_length=20,
                               verbose_name='Отчество',
                               null=False,
                               blank=False)
    
    age = models.SmallIntegerField(validators=[MinValueValidator(18), 
                                               MaxValueValidator(99)],
                                        null=False,
                                        blank=False,
                                        verbose_name='Возраст')
    
    gender = models.CharField(choices=[('m', 'Мужской'), ('f', 'Женский')],
                                 null=True,
                                 blank=True, 
                                 verbose_name='Пол')
    
    courses = models.ManyToManyField(to='Course',
                                    blank=True,
                                    verbose_name='Посещаемые курсы',
                                    related_name='students')
    
    photo = models.ImageField(upload_to='students/photos/',
                              blank=True,
                              null=True,
                              verbose_name='Фотография',
                              help_text='Загрузите фото или оставьте пустым для авто-уточки')
    
    slug = models.SlugField(unique=True, blank=True, verbose_name='url-slug')
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Пользователь', related_name='student_profile')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = ruslugify(f"{self.surname}-{self.name}")

        original_slug = self.slug
        counter = 1

        while Student.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.surname} {self.name}'
    
    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'slug':self.slug})
    
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        indexes = [models.Index(fields=['surname'])]
        ordering = ['surname']

class Teacher(models.Model):
    name = models.CharField(max_length=20,
                            verbose_name='Имя',
                            null=False,
                            blank=False)
    
    surname = models.CharField(max_length=20,
                               verbose_name='Фамилия',
                               null=False,
                               blank=False)
    
    second_name = models.CharField(max_length=20,
                               verbose_name='Отчество',
                               null=False,
                               blank=False)
    
    age = models.SmallIntegerField(validators=[MinValueValidator(18), 
                                               MaxValueValidator(99)],
                                        null=False,
                                        blank=False,
                                        verbose_name='Возраст')
    
    gender = models.CharField(choices=[('m', 'Мужской'), ('f', 'Женский')],
                                 null=True,
                                 blank=True, 
                                 verbose_name='Пол')
    
    courses = models.ManyToManyField(to='Course',
                                    blank=True,
                                    verbose_name='Преподаваемые курсы',
                                    related_name='teachers')
    
    photo = models.ImageField(upload_to='teachers/photos/',
                              blank=True,
                              null=True,
                              verbose_name='Фотография',
                              help_text='Загрузите фото или оставьте пустым для авто-лисички')
    
    slug = models.SlugField(unique=True, blank=True, verbose_name='url-slug')
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Пользователь', related_name='teacher_profile')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = ruslugify(f"{self.surname}-{self.name}")

        original_slug = self.slug
        counter = 1

        while Teacher.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.surname} {self.name}'
    
    def get_absolute_url(self):
        return reverse('teacher_detail', kwargs={'slug':self.slug})
    
    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        indexes = [models.Index(fields=['surname'])]
        ordering = ['surname']

class Course(models.Model):
    langs = [
        ('py', 'Python'),
        ('ja', 'Java'),
        ('js', 'JavaScript'),
        ('cpp', 'C++'),
        ('csh', 'C#'),
        ('an', 'Android')
    ]

    name = models.CharField(choices=langs,
                            verbose_name='Курс',
                            null=False,
                            blank=False)
    
    course_num = models.SmallIntegerField(default=1,
                                          verbose_name='Номер курса',
                                          validators=[MinValueValidator(1),
                                                      MaxValueValidator(100)],)
    
    start_date = models.DateField(verbose_name='Дата начала',
                                  null=True)
    
    end_date = models.DateField(verbose_name='Дата окончания',
                                null=True)
    
    description = models.TextField(verbose_name='Описание', blank=True)

    slug = models.SlugField(unique=True, blank=True, verbose_name='url-slug')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.course_num}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.course_num}'
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug':self.slug})
    
    class Meta:
        unique_together = [['name', 'course_num']]
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['name', 'course_num']


class Grade(models.Model):
    grade = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),
                                                         MaxValueValidator(10),],
                                                         default=0,
                                                         null=True,
                                                         verbose_name='Оценка')
    
    student = models.ForeignKey(Student,
                               on_delete=models.CASCADE,
                               related_name='Grades',
                               verbose_name='Студент')
    
    course = models.ForeignKey(Course,
                               related_name='Course',
                               on_delete=models.CASCADE,
                               verbose_name='Курс')
    
    date = models.DateField(verbose_name='Дата оценки', null=True)

    date_add = models.DateField(auto_now_add=True,
                                null=True,
                                verbose_name='Дата добавления')
    
    date_update = models.DateField(auto_now=True,
                                   verbose_name='Дата изменения',
                                   null=True)
    
    slug = models.SlugField(unique=True, blank=True, verbose_name='url-slug')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = ruslugify(f"{self.student.slug}-{self.course.slug}-{self.date.day}{self.date.month}{self.date.year}")

        original_slug = self.slug
        counter = 1

        while Grade.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        ordering = ['-date']

class InvitationCode(models.Model):
    code = models.CharField(max_length=32, unique=True, verbose_name='Пригласительный код')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    expires_at = models.DateTimeField(verbose_name='Действитилен до')
    is_used = models.BooleanField(default=False, verbose_name='Использован')
    used_by = models.CharField(max_length=150, blank=True, null=True, verbose_name='Использован пользователем')
    used_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата использования')

    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Студент', related_name='student_invite')

    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Преподаватель', related_name='teacher_invite')
    
    class Meta:
        verbose_name = 'Пригласительный код'
        verbose_name_plural = 'Пригласительные коды'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.code} - {self.group}'
    
    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at
    
    def get_profile(self):
        return self.student or self.teacher

    @staticmethod
    def generate_code(length=20):
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @classmethod
    def create_code(cls, group_name, hours=1, student=None, teacher=None):
        group = Group.objects.get(name=group_name)
        code = cls.generate_code()
        expires_at = timezone.now() + timedelta(hours=hours)
        
        return cls.objects.create(code=code, group=group, expires_at=expires_at, student=student, teacher=teacher)
    
    @classmethod
    def delete_expired(cls):
        expired = cls.objects.filter(expires_at__lt=timezone.now())
        expired.delete()