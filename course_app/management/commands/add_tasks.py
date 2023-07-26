
from datetime import datetime, timedelta

from django.core.management import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Command(BaseCommand):
    def handle(self, *args, **options):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS,
        )

        PeriodicTask.objects.create(
            interval=schedule,
            name='Check payment status',
            task='course_app.tasks.check_status_payment',
            expires=datetime.now() + timedelta(seconds=30)
        )
