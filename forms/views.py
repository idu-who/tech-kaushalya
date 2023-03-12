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
        team_id = request.session.get('team_id')
        member_name_input = request.POST.get('member_name').strip()
        email_input = request.POST.get('email').strip()
        mobile_input = request.POST.get('mobile').strip()
        context['form'] = {
            'member_name': member_name_input,
            'email': email_input,
            'mobile': mobile_input
        }

        if event.is_team_event:
            if not team_id and not request.POST.get('cancel'):
                team = Team(event=event)
                team.save()
                request.session['team_id'] = team.id
            else:
                try:
                    team = Team.objects.get(id=team_id)
                except ObjectDoesNotExist:
                    if team_id:
                        del request.session['team_id']
                    messages.error(request, 'Team does not exist.')
                    return redirect('home')

            if request.POST.get('cancel'):
                team.delete()
                if team_id:
                    del request.session['team_id']
                return redirect('home')

            members = Member.objects.filter(team=team)
            member = Member(
                team=team,
                member_name=member_name_input,
                email=email_input,
                mobile=mobile_input,
                is_registrant=not members.count()
            )
            try:
                if members.count() >= event.max_team_members:
                    messages.error(request, 'Team is already full.')
                    return redirect('home')

                error_dict = {}
                is_email_registered = Member.objects.filter(
                    team__event=event,
                    email=email_input
                ).exists()
                if is_email_registered:
                    error_dict['email'] = ('Email has already been registed to'
                                           ' this event.')

                is_mobile_registered = Member.objects.filter(
                    team__event=event,
                    mobile=mobile_input
                ).exists()
                if is_mobile_registered:
                    error_dict['mobile'] = ('Mobile number has already been '
                                            'registed to this event.')

                if error_dict:
                    raise ValidationError(error_dict)

                member.full_clean()
                member.save()
                messages.success(request, 'Registered to event successfully.')
                del context['form']
            except ValidationError as e:
                if hasattr(e, 'error_dict'):
                    context['errors'] = e.message_dict.items()
                else:
                    context['errors'] = [('__all__', e)]

            if request.POST.get('add') or context.get('errors'):
                context['members'] = members
            else:
                return redirect('home')
        else:
            team = Team.objects.get_or_create(event=event)
            if not team_id and not request.POST.get('cancel'):
                team = Team(event=event)
                team.save()
                request.session['team_id'] = team.id
            else:
                try:
                    team = Team.objects.get(id=team_id)
                except ObjectDoesNotExist:
                    if team_id:
                        del request.session['team_id']
                    messages.error(request, 'Team does not exist.')
                    return redirect('home')

            if request.POST.get('cancel'):
                team.delete()
                if team_id:
                    del request.session['team_id']
                return redirect('home')

            member = Member(
                team=team,
                member_name=member_name_input,
                email=email_input,
                mobile=mobile_input,
                is_registrant=True
            )
            try:
                error_dict = {}
                is_email_registered = Member.objects.filter(
                    team__event=event,
                    email=email_input
                ).exists()
                if is_email_registered:
                    error_dict['email'] = ('Email has already'
                                           ' been registed to this event.')

                is_mobile_registered = Member.objects.filter(
                    team__event=event,
                    mobile=mobile_input
                ).exists()
                if is_mobile_registered:
                    error_dict['mobile'] = ('Mobile number'
                                            'has already been registed to this'
                                            ' event.')

                if error_dict:
                    raise ValidationError(error_dict)

                member.full_clean()
                member.save()
                messages.success(request, 'Registered to event successfully.')
                return redirect('home')
            except ValidationError as e:
                team.delete()
                if hasattr(e, 'error_dict'):
                    context['errors'] = e.message_dict.items()
                else:
                    context['errors'] = [('__all__', e)]

    return render(request, template_name, context)
