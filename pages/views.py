from django.conf import settings
from django.shortcuts import render
from forms.models import Event

# Create your views here.


def home_view(request):
    context = {}
    return render(request, 'pages/home.html', context)


def schedule_view(request, day):
    date = settings.DAY1_DATE if day == 1 else settings.DAY2_DATE
    events = Event.objects.filter(schedule__date=date).order_by('schedule')
    context = {
        'day': day,
        'tech_events': events.filter(is_tech_event=True),
        'non_tech_events': events.filter(is_tech_event=False),
    }
    return render(request, 'pages/schedule.html', context)
