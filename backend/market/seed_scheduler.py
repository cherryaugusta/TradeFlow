from django_celery_beat.models import IntervalSchedule, PeriodicTask


def seed_periodic_task():
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=5,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.update_or_create(
        name="Poll mock exchanges every 5 seconds",
        defaults={
            "interval": schedule,
            "task": "market.tasks.poll_mock_exchanges",
            "enabled": True,
        },
    )
