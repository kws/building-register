from django.core.management import BaseCommand

from register.tasks import send_reminders


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--send', action="store_true")

    def handle(self, *args, send, **options):
        send_reminders(send)