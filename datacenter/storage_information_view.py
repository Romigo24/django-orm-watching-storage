from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import format_duration, get_duration, is_visit_long
from django.utils.timezone import localtime

def storage_information_view(request):
    open_visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    for visit in open_visits:
        duration = get_duration(visit)
        non_closed_visits.append({
            'who_entered': visit.passcard.owner_name,
            'entered_at': localtime(visit.entered_at),
            'duration': format_duration(duration),
            'is_strange': is_visit_long(visit, minutes=60)
        })

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
