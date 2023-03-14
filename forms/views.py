from django.contrib import messages
from django.core.exceptions import (
    ValidationError,
    ObjectDoesNotExist,
    NON_FIELD_ERRORS
)
from django.db import DatabaseError, transaction
from django.shortcuts import render, redirect

from .models import (
    Updates_mail_list,
    Event,
    Team,
    Member
)

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


def is_duplicate(member, emails, mobiles):
    error_dict = {}

    if (member.email in emails):
        error_dict['email'] = ('Email is a duplicate of other team member\'s '
                               'email.')

    if (member.mobile in mobiles):
        error_dict['mobile'] = ('Mobile is a duplicate of other team member\'s'
                                ' mobile.')

    emails.append(member.email)
    mobiles.append(member.mobile)

    if error_dict:
        raise ValidationError(error_dict)


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
    post_data = request.POST
    field_names = {field.name for field in Member._meta.fields} - \
        {'id', 'team', 'is_registrant'}
    emails = []
    mobiles = []
    valid_members = []
    upi_reference_number_input = request.POST.get('upi_reference_number',
                                                  '').strip()
    context['form'] = {
        'upi_reference_number': upi_reference_number_input
    }

    for member_no in range(1, event.max_team_members+1):
        name_template = f'member{member_no}_{{}}'
        input_names = [name_template.format(field_name)
                       for field_name in field_names]
        name_map = dict(zip(field_names, input_names))

        member_data = {field_name: post_data.get(input_name, '').strip()
                       for field_name, input_name in name_map.items()}

        if not any(member_data.values()):
            continue

        context['form'].update({
            member_no: member_data
        })

        member = Member(
            **member_data,
            is_registrant=not member_no-1
        )

        try:
            member.full_clean()
            is_duplicate(member, emails, mobiles)
            is_member_registered(member, event)
            valid_members.append(member)
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                input_name_message_dict = {name_map[field_name]: error_list
                                           for field_name, error_list
                                           in e.message_dict.items()}
                context.setdefault('errors', []).extend(
                    list(input_name_message_dict.items()))
            else:
                context['errors'] = [(
                    name_template.format(NON_FIELD_ERRORS), e)]

    if len(valid_members) < event.min_team_members:
        msg_template = ('Event requires a minimum of {} team members.'
                        ' You provided only {} valid team member\'s')
        messages.error(request, msg_template.format(event.min_team_members,
                                                    len(valid_members)))
        return

    try:
        team = Team(
            event=event, upi_reference_number=upi_reference_number_input)
        try:
            with transaction.atomic():
                team.full_clean()
                team.save()
                for member in valid_members:
                    member.team = team
                    member.save()
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                context['errors'] = e.message_dict.items()
            else:
                context['errors'] = [(NON_FIELD_ERRORS, e)]
            return
        del context['form']
        messages.success(request, 'Registration successful.')
    except DatabaseError as e:
        messages.error(request, 'Error: '+e.__cause__)


def individual_registration_handler(request, context, event):
    member_name_input = request.POST.get('member_name', '').strip()
    email_input = request.POST.get('email', '').strip()
    mobile_input = request.POST.get('mobile', '').strip()
    university_name_input = request.POST.get('university_name', '').strip()
    course_name_input = request.POST.get('course_name', '').strip()
    residence_area_input = request.POST.get('residence_area', '').strip()
    upi_reference_number_input = request.POST.get('upi_reference_number','').strip()
    context['form'] = {
        'member_name': member_name_input,
        'email': email_input,
        'mobile': mobile_input,
        'university_name': university_name_input,
        'course_name': course_name_input,
        'residence_area': residence_area_input,
        'upi_reference_number': upi_reference_number_input
    }

    member = Member(
        member_name=member_name_input,
        email=email_input,
        mobile=mobile_input,
        university_name=university_name_input,
        course_name=course_name_input,
        residence_area=residence_area_input,
        is_registrant=True
    )

    try:
        try:
            member.full_clean()
            is_member_registered(member, event)
            team = Team(
                event=event, upi_reference_number=upi_reference_number_input)
            with transaction.atomic():
                team.full_clean()
                team.save()
                member.team = team
                member.save()
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                context['errors'] = e.message_dict.items()
            else:
                context['errors'] = [(NON_FIELD_ERRORS, e)]
            return
        del context['form']
        messages.success(request, 'Registration successful.')
    except DatabaseError as e:
        messages.error(request, 'Error: '+e.__cause__)


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
