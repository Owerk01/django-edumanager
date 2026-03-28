from django.core.management.base import BaseCommand
from main.models import InvitationCode

class Command(BaseCommand):
    help = "Удалить пригласительные коды с истёкшим сроком действия"
    def handle(self, *args, **options):
        InvitationCode.delete_expired()
        self.stdout.write(self.style.SUCCESS(f'Все пригласительные коды с истёкшим сроком действия удалены'))