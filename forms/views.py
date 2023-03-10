from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from .models import (
    Updates_mail_list,
    # Event,
    # Team,
    # Member,
    # Payment
)

# Create your views here.


def updates_submit_view(request):
    referer_url = request.META.get('HTTP_REFERER')

    if request.POST:
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


def register_view(request, event_name):
    context = {}
    template_name = 'forms/individual_form.html'  # 'forms/team_form.html'
    if request.POST:
        pass
    return render(request, template_name, context)
