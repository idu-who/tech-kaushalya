from django.shortcuts import render

# Create your views here.


def home_view(request):
    context = {}
    # if request.GET:
    #     pass
    # else if request.POST:
    #     pass
    return render(request, 'pages/home.html', context)
