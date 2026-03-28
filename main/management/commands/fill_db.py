from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import connection
from main.models import Student, Teacher, Course, Grade
from datetime import date, timedelta
import random
import asyncio
import httpx
from pathlib import Path

def clean_ducks():
    photos_dir = Path(settings.MEDIA_ROOT) / "students" / "photos"
    if not photos_dir.exists():
        print("Папки с фотографиями студентов не существует, удаление пропускается")
        return

    for file_path in photos_dir.glob("duck_*.jpg"):
        try:
            file_path.unlink()
        except Exception as e:
            print(f"Ошибка при удалении файла {file_path}: {e}")

def clean_foxes():
    photos_dir = Path(settings.MEDIA_ROOT) / "teachers" / "photos"
    if not photos_dir.exists():
        print("Папки с фотографиями преподавателей не существует, удаление пропускается")
        return

    for file_path in photos_dir.glob("fox_*.jpg"):
        try:
            file_path.unlink()
        except Exception as e:
            print(f"Ошибка при удалении файла {file_path}: {e}")

def reset_database_ids(): 
    with connection.cursor() as cursor:
        tables = ['student', 'teacher', 'course', 'grade', 'invitationcode']
        for table in tables:
            try:
                cursor.execute(f"ALTER SEQUENCE main_{table}_id_seq RESTART WITH 1")
            except Exception:
                pass

async def get_duck(client: httpx.AsyncClient):
    try:
        res = await client.get("https://random-d.uk/api/random", timeout=7)
        res.raise_for_status()
        json_ = res.json()
        url = json_.get("url")
        
        if not url:
            return None
        
        image = await client.get(url, timeout=7, follow_redirects=True)
        image.raise_for_status()

        num = url.split('/')[-1].split('.')[0] or random.randint(1000, 9999)
        filename = f"duck_{num}.jpg"

        return ContentFile(image.content, name=filename)
    except Exception as e:
        print(f"Не удалось загрузить уточку: {e}")
        return None

async def get_fox(client: httpx.AsyncClient):
    try:
        res = await client.get("https://randomfox.ca/floof", timeout=7, follow_redirects=True)
        res.raise_for_status()
        json_ = res.json()
        url = json_.get("image")
        
        if not url:
            return None
        
        image = await client.get(url, timeout=7, follow_redirects=True)
        image.raise_for_status()

        num = url.split('/')[-1].split('.')[0] or random.randint(1000, 9999)
        filename = f"fox_{num}.jpg"

        return ContentFile(image.content, name=filename)
    except Exception as e:
        print(f"Не удалось загрузить лисичку: {e}")
        return None

async def get_ducks(count: int):
    async with httpx.AsyncClient() as client:
        tasks = [get_duck(client) for _ in range(count)]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]

async def get_foxes(count: int):
    async with httpx.AsyncClient() as client:
        tasks = [get_fox(client) for _ in range(count)]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]

class Command(BaseCommand):
    help = 'Наполняет базу тестовыми данными (студенты с уточками, преподаватели с лисами)'
    
    def add_arguments(self, parser):
        parser.add_argument('--students', type=int, default=48, help='Кол-во студентов')
        parser.add_argument('--teachers', type=int, default=16, help='Кол-во преподавателей')
        parser.add_argument('--grades', type=int, default=144, help='Кол-во оценок')
        parser.add_argument('--reset-ids', action='store_true', help='Сбросить ID на 1')

    def handle(self, *args, **options):
        num_students = options['students']
        num_teachers = options.get('teachers', 5)
        num_grades = options['grades']
        reset_ids = options.get('reset_ids', False)

        self.stdout.write(self.style.WARNING('Очищаем базу...'))
        Grade.objects.all().delete()
        Student.objects.all().delete()
        Teacher.objects.all().delete()
        Course.objects.all().delete()

        if reset_ids:
            self.stdout.write(self.style.WARNING('Сбрасываем автоинкремент ID...'))
            reset_database_ids()
            self.stdout.write(self.style.SUCCESS('  ✓ ID сброшены'))

        clean_ducks()
        clean_foxes()

        self.stdout.write('Создаём курсы...')
        courses_data = [
            {'name': 'py', 'course_num': 1, 'desc': 'Основы Python для чайников'},
            {'name': 'py', 'course_num': 2, 'desc': 'Основы Python для чайников'},
            {'name': 'js', 'course_num': 1, 'desc': 'JavaScript с нуля'},
            {'name': 'js', 'course_num': 2, 'desc': 'JavaScript с нуля'},
            {'name': 'cpp', 'course_num': 1, 'desc': 'C++ для самых стойких'},
            {'name': 'csh', 'course_num': 1, 'desc': 'C# для смелых'},
            {'name': 'ja', 'course_num': 1, 'desc': 'Java для корпоративных джедаев'},
            {'name': 'an', 'course_num': 1, 'desc': 'Разработка под Android'},
        ]

        courses = []
        for c in courses_data:
            course = Course.objects.create(
                name=c['name'],
                course_num=c['course_num'],
                description=c['desc'],
                start_date=date.today() - timedelta(days=random.randint(30, 100)),
                end_date=date.today() + timedelta(days=random.randint(10, 50))
            )
            courses.append(course)
            self.stdout.write(self.style.SUCCESS(f'   Курс {course}'))

        male_names = ['Иван', 'Пётр', 'Алексей', 'Дмитрий', 'Сергей', 'Александр', 'Николай', 'Андрей', 'Михаил', 'Владимир']
        female_names = ['Анна', 'Мария', 'Елена', 'Ольга', 'Наталья', 'Екатерина', 'Татьяна', 'Ирина', 'Светлана', 'Юлия']
        
        male_surnames = ['Иванов', 'Петров', 'Сидоров', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Михайлов', 'Новиков', 'Фёдоров']
        female_surnames = ['Иванова', 'Петрова', 'Сидорова', 'Смирнова', 'Кузнецова', 'Попова', 'Васильева', 'Михайлова', 'Новикова', 'Фёдорова']
        
        male_patronymics = ['Иванович', 'Петрович', 'Сергеевич', 'Алексеевич', 'Дмитриевич', 'Александрович', 'Николаевич', 'Андреевич', 'Михайлович', 'Владимирович']
        female_patronymics = ['Ивановна', 'Петровна', 'Сергеевна', 'Алексеевна', 'Дмитриевна', 'Александровна', 'Николаевна', 'Андреевна', 'Михайловна', 'Владимировна']

        self.stdout.write(f'Скачиваем {num_students} уточек...')
        duck_photos = asyncio.run(get_ducks(num_students))
        self.stdout.write(self.style.SUCCESS(
            f'  Скачано {len(duck_photos)} уточек'
        ))

        self.stdout.write('Создаём студентов...')
        students = []
        for i in range(num_students):
            gender = random.choice(['m', 'f'])

            if gender == 'm':
                name = random.choice(male_names)
                surname = random.choice(male_surnames)
                second_name = random.choice(male_patronymics)
            else:
                name = random.choice(female_names)
                surname = random.choice(female_surnames)
                second_name = random.choice(female_patronymics)
            
            photo = duck_photos[i] if i < len(duck_photos) else None

            student = Student.objects.create(
                name=name,
                surname=surname,
                second_name=second_name,
                age=random.randint(18, 35),
                gender=gender,
                photo=photo
            )

            num_courses = random.randint(1, 3)
            student_courses = random.sample(courses, min(num_courses, len(courses)))
            student.courses.set(student_courses)
            
            students.append(student)
            self.stdout.write(self.style.SUCCESS(f'  Студент {student} ({student.get_gender_display()})'))

        self.stdout.write(f'Скачиваем {num_teachers} лисичек асинхронно...')
        fox_photos = asyncio.run(get_foxes(num_teachers))
        self.stdout.write(self.style.SUCCESS(
            f'  Скачано {len(fox_photos)} лисичек'
        ))

        self.stdout.write('Создаём преподавателей...')
        teachers = []
        for i in range(num_teachers):
            gender = random.choice(['m', 'f'])

            if gender == 'm':
                name = random.choice(male_names)
                surname = random.choice(male_surnames)
                second_name = random.choice(male_patronymics)
            else:
                name = random.choice(female_names)
                surname = random.choice(female_surnames)
                second_name = random.choice(female_patronymics)

            photo = fox_photos[i] if i < len(fox_photos) else None

            teacher = Teacher.objects.create(
                name=name,
                surname=surname,
                second_name=second_name,
                age=random.randint(25, 60),  
                gender=gender,
                photo=photo
            )

            num_courses = random.randint(1, 2)
            teacher_courses = random.sample(courses, min(num_courses, len(courses)))
            teacher.courses.set(teacher_courses)
            
            teachers.append(teacher)
            self.stdout.write(self.style.SUCCESS(f'   Преподаватель {teacher} ({teacher.get_gender_display()})'))

        self.stdout.write('Создаём оценки...')
        grades_created = 0
        attempts = 0
        max_attempts = num_grades * 10

        while grades_created < num_grades and attempts < max_attempts:
            student = random.choice(students)
            course = random.choice(courses)
            
            if course in student.courses.all():
                Grade.objects.create(
                    student=student,
                    course=course,
                    grade=random.randint(3, 10),
                    date=date.today() - timedelta(days=random.randint(0, 60))
                )
                grades_created += 1
            attempts += 1

        self.stdout.write(self.style.SUCCESS(f'  Попыток: {attempts}, Успешно: {grades_created}'))
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('База наполнена:'))
        self.stdout.write(f'   Студентов: {Student.objects.count()}')
        self.stdout.write(f'   Преподавателей: {Teacher.objects.count()}')
        self.stdout.write(f'   Курсов: {Course.objects.count()}')
        self.stdout.write(f'   Оценок: {Grade.objects.count()}')
        self.stdout.write(self.style.SUCCESS('='*50 + '\n'))