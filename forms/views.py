from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import redirect, render

from forms.handlers import (individual_registration_handler,
                            team_registration_handler)

from .models import Event, Updates_mail_list

# Create your views here.


def updates_submit_view(request):
    referer_url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        email_input = request.POST.get('email', '').strip()
        try:
            updates_email = Updates_mail_list(email=email_input)
            updates_email.full_clean()
            updates_email.save()
            messages.success(request, 'Signed up to receive updates '
                             'successfully.')
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                for error_list in e.message_dict.values():
                    for error in error_list:
                        messages.error(request, error)
            else:
                messages.error(request, e)
        return redirect(referer_url)

    return redirect('home')


def register_view(request, event_id):
    context = {}

    try:
        event = Event.objects.get(id=event_id)
        context['event'] = event
    except ObjectDoesNotExist:
        messages.error(request, 'Event does not exist.')
        return redirect('home')

    if not event.is_registration_open:
        messages.info(request, f'Registrations for {event.event_name} are'
                      ' closed.')
        return redirect('home')

    if event.is_team_event:
        template_name = 'forms/team_registration.html'
        context.update({
            'required_member_nos': range(1, event.min_team_members+1),
            'optional_member_nos': range(event.min_team_members+1,
                                         event.max_team_members+1)
        })
    else:
        template_name = 'forms/individual_registration.html'

    if request.method == 'POST':
        if event.is_team_event:
            team_registration_handler(request, context, event)
        else:
            individual_registration_handler(request, context, event)

    return render(request, template_name, context)
