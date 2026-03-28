from django.core.management.base import BaseCommand
from main.models import InvitationCode, Student, Teacher
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import timedelta
import secrets
import string

class Command(BaseCommand):
    help = "Генерирует пригласительный код"
    
    def add_arguments(self, parser):
        parser.add_argument('group', type=str, help='Группа (student, teacher, director, admin)')
        parser.add_argument('--hours', type=int, default=1, help='Срок действия в часах')
        parser.add_argument('--profile-id', type=int, help='ID профиля')

    def handle(self, *args, **options):
        group_map = {
            'student': ('Students', Student),
            'teacher': ('Teachers', Teacher),
            'director': ('Directors', None),  
            'admin': ('Admins', None),  
        }

        group_name = options['group']
        if group_name not in group_map:
            available = ', '.join(group_map.keys())
            self.stdout.write(self.style.ERROR(f'Указана неверная группа {group_name}. Доступны: {available}'))
            return
        
        real_group_name, model = group_map[group_name]
        hours = options['hours']
        profile_id = options.get('profile_id')
        student = None
        teacher = None

        group, created = Group.objects.get_or_create(name=real_group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа {real_group_name} создана'))

        if profile_id and model:
            try:
                profile = model.objects.get(id=profile_id)
                if model == Student:
                    student = profile
                else:
                    teacher = profile
                self.stdout.write(self.style.SUCCESS(f'Код привязан к профилю: {profile}'))
            except model.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Профиль с ID {profile_id} не найден'))
                return
        elif profile_id and not model:
            self.stdout.write(self.style.WARNING(f'Для группы {real_group_name} нельзя привязать профиль'))

        code = self.generate_code()
        expires_at = timezone.now() + timedelta(hours=hours)
        
        code_obj = InvitationCode.objects.create(
            code=code,
            group=group,
            expires_at=expires_at,
            student=student,
            teacher=teacher
        )
        
        self.stdout.write(self.style.SUCCESS(f'Код: {code_obj.code}'))
        self.stdout.write(self.style.SUCCESS(f'Действителен до: {code_obj.expires_at}'))
        self.stdout.write(self.style.SUCCESS(f'Группа: {code_obj.group.name}'))
        if student:
            self.stdout.write(self.style.SUCCESS(f'Студент: {student}'))
        if teacher:
            self.stdout.write(self.style.SUCCESS(f'Преподаватель: {teacher}'))
    
    def generate_code(self, length=20):
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))