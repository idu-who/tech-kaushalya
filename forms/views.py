from django.contrib import messages
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render, redirect

from .models import (
    Updates_mail_list,
    Event,
    Team,
    Member,
    Payment
)

# Create your views here.


def updates_submit_view(request):
    referer_url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        email_input = request.POST.get('email').strip()
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


def is_member_registered(member, event):
    error_dict = {}

    is_email_registered = Member.objects.filter(
        team__event=event,
        email=member.email
    ).exists()
    if is_email_registered:
        error_dict['email'] = ('Email has already been registed to for this '
                               'event.')

    is_mobile_registerer = Member.objects.filter(
        team__event=event,
        mobile=member.mobile
    ).exists()
    if is_mobile_registerer:
        error_dict['mobile'] = ('Mobile number has already been registed for '
                                'this event.')

    if error_dict:
        raise ValidationError(error_dict)


def team_registration_handler(request, context, event):
    pass


def individual_registration_handler(request, context, event):
    member_name_input = request.POST.get('member_name').strip()
    email_input = request.POST.get('email').strip()
    mobile_input = request.POST.get('mobile').strip()
    context['form'] = {
        'member_name': member_name_input,
        'email': email_input,
        'mobile': mobile_input
    }

    member = Member(
        member_name=member_name_input,
        email=email_input,
        mobile=mobile_input,
        is_registrant=True
    )

    try:
        member.full_clean()
        is_member_registered(member, event)
        team = Team(event=event)
        team.save()
        member.team = team
        member.save()
        del context['form']
        messages.success(request, 'Registration successful.')
    except ValidationError as e:
        if hasattr(e, 'error_dict'):
            context['errors'] = e.message_dict.items()
        else:
            context['errors'] = [('__all__', e)]


def register_view(request, event_id):
    context = {}

    try:
        event = Event.objects.get(id=event_id)
        context['event'] = event
    except ObjectDoesNotExist:
        messages.error(request, 'Event does not exist.')
        return redirect('home')

    template_name = ('forms/team_form.html' if event.is_team_event else
                     'forms/individual_form.html')

    if request.method == 'POST':
        if event.is_team_event:
            team_registration_handler(request, context, event)
        else:
            individual_registration_handler(request, context, event)

    return render(request, template_name, context)
