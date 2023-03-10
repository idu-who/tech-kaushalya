from django.shortcuts import render
from forms.models import Event

from datetime import datetime

# Create your views here.


def home_view(request):
    context = {}
    return render(request, 'pages/home.html', context)


def day1_view(request):
    day1_events = Event.objects.filter(schedule__date=datetime(2023, 3, 20))
    context = {
        'tech_events': day1_events.filter(is_tech_event=True),
        'non_tech_events': day1_events.filter(is_tech_event=False)
    }
    print(day1_events)
    return render(request, 'pages/day-1.html', context)


def day2_view(request):
    day2_events = Event.objects.filter(schedule__date=datetime(2023, 3, 21))
    context = {
        'tech_events': day2_events.filter(is_tech_event=True),
        'non_tech_events': day2_events.filter(is_tech_event=False)
    }
    return render(request, 'pages/day-2.html', context)
