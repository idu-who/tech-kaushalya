from django.contrib import messages
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import DatabaseError, transaction

from .models import Member, Team


def check_duplicate(member, team_member_emails, team_member_mobiles):
    """Check if a given member's email or mobile number is a duplicate of
    another team member's email or mobile number.

    Args:
        member (Member): Member to check.
        team_member_emails (list): Other team member's emails.
        team_member_mobiles (list): Other team member's mobile numbers.

    Raises:
        ValidationError: If the given member's email or mobile number already
                         exists in the list of emails or mobiles.
    """
    error_dict = {}

    if (member.email in team_member_emails):
        error_dict['email'] = ("Email is a duplicate of other team member's "
                               "email.")

    if (member.mobile in team_member_mobiles):
        error_dict['mobile'] = ("Mobile is a duplicate of other team member's"
                                " mobile.")

    team_member_emails.append(member.email)
    team_member_mobiles.append(member.mobile)

    if error_dict:
        raise ValidationError(error_dict)


def check_member_registered(member, event):
    """Check if a given member's email or mobile number is already registered
    for a particular event.

    Args:
        member (Member): Member to check.
        event (Event): Event for which the member is registering.

    Raises:
        ValidationError: If the given member's email or mobile number is
                         already registered for the event.
    """
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
    """Handle team registration for an event.

    Args:
        request (HttpRequest): A Django request object.
        context (dict): A dictionary containing the context data for the
                        template.
        event (Event): Event for which the team is registering.
    """
    post_data = request.POST
    field_names = {field.name for field in Member._meta.fields} - \
        {'id', 'team', 'is_registrant'}
    upi_reference_number_input = post_data.get('upi_reference_number',
                                               '').strip()
    context['form'] = {'upi_reference_number': upi_reference_number_input}
    team_member_emails = []
    team_member_mobiles = []
    valid_members = []

    for member_no in range(1, event.max_team_members+1):
        # using template and field_names to get input_names
        name_template = f'member{member_no}_{{}}'
        input_names = [name_template.format(field_name)
                       for field_name in field_names]
        # mapping input_names to field_names
        name_map = dict(zip(field_names, input_names))

        # getting form_data
        form_data = {field_name: post_data.get(input_name, '').strip()
                     for field_name, input_name in name_map.items()}

        context['form'].update({member_no: form_data})
        # is_registrant is True only for member 1
        member = Member(**form_data, is_registrant=not member_no-1)

        try:
            member.full_clean()
            check_duplicate(member, team_member_emails, team_member_mobiles)
            check_member_registered(member, event)
            valid_members.append(member)
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                # creating message_dict with field_name replaced by input_name
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
        team = Team(event=event,
                    upi_reference_number=upi_reference_number_input)
        team.full_clean()

        with transaction.atomic():
            team.save()
            for member in valid_members:
                member.team = team
                member.save()
        del context['form']
        messages.success(request, 'Registration successful.')
    except ValidationError as e:
        if hasattr(e, 'error_dict'):
            context['errors'] = e.message_dict.items()
        else:
            context['errors'] = [(NON_FIELD_ERRORS, e)]
    except DatabaseError as e:
        messages.error(request, 'Error: '+e.__cause__)


def individual_registration_handler(request, context, event):
    """Handle individual registration handler.

    Args:
        request (HttpRequest): A Django request object.
        context (dict): A dictionary containing the context data for the
                        template.
        event (Event): Event for which the member is registering.
    """
    form_data = {
        'member_name': request.POST.get('member_name', '').strip(),
        'email': request.POST.get('email', '').strip(),
        'mobile': request.POST.get('mobile', '').strip(),
        'university_name': request.POST.get('university_name', '').strip(),
        'course_name': request.POST.get('course_name', '').strip(),
        'residence_area': request.POST.get('residence_area', '').strip()
    }
    upi_reference_number_input = request.POST.get('upi_reference_number',
                                                  '').strip()
    context['form'] = form_data

    member = Member(**form_data, is_registrant=True)

    try:
        member.full_clean()
        check_member_registered(member, event)

        team = Team(event=event,
                    upi_reference_number=upi_reference_number_input)
        team.full_clean()

        with transaction.atomic():
            team.save()
            member.team = team
            member.save()

        del context['form']
        messages.success(request, 'Registration successful.')
    except ValidationError as e:
        if hasattr(e, 'error_dict'):
            context['errors'] = e.message_dict.items()
        else:
            context['errors'] = [(NON_FIELD_ERRORS, e)]
    except DatabaseError as e:
        messages.error(request, 'Error: '+e.__cause__)
