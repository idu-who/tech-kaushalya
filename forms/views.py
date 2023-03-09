from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.


def updates_submit_view(request):
    referer_url = request.META.get('HTTP_REFERER')

    if request.POST:
        email_input = request.POST.get('email')
        try:
            # register email for updates and handle errors
            messages.success(request, 'Signed up to receive updates '
                             'successfully.')
            # raise Exception('Invalid email.')
        except Exception as e:
            messages.error(request, e)
        return redirect(referer_url)

    return redirect('home')


def register_view(request, event):
    if request.GET:
        context = {}
        template_name = 'forms/individual_form.html'
        render(request, template_name, context)
