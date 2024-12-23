from django.db import models
from django.utils.timezone import localtime
import datetime


SECONDS_IN_ONE_HOURS = 3600
SECONDS_IN_ONE_MINUTES = 60


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

def is_visit_long(visit, minutes=60):
    return get_duration(visit) > datetime.timedelta(minutes=minutes)

def get_duration(visit):
    if visit.leaved_at:
        delta = visit.leaved_at - visit.entered_at
    else:
        delta = localtime() - visit.entered_at
    return delta

def format_duration(delta):
    total_seconds = delta.total_seconds()
    hours = int(total_seconds // SECONDS_IN_ONE_HOURS)
    minutes = int((total_seconds % SECONDS_IN_ONE_HOURS) // SECONDS_IN_ONE_MINUTES)
    seconds = int(total_seconds % SECONDS_IN_ONE_MINUTES)
    return '{hours}:{minutes:02d}:{seconds:02d}'.format(
        hours=hours,
        minutes=minutes,
        seconds=seconds
    )