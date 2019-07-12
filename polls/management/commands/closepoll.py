from django.core.management.base import BaseCommand
from bonuses import models
from datetime import date


class Command(BaseCommand):
    help = 'Closes the specified polls for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        today = date.today()
        operations = models.Operation.objects.all()
        for operation in operations:
            if operation.expiration_date is None:
                continue
            if operation.expiration_date < today:
                operation.delete()
