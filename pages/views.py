from django.shortcuts import render

# Create your views here.


def home_view(request):
    context = {}
    return render(request, 'pages/home.html', context)


def day1_view(request):
    context = {}
    # if request.GET:
    #     pass
    # else if request.POST:
    #     pass
    return render(request, 'pages/day-1.html', context)


def day2_view(request):
    context = {}
    # if request.GET:
    #     pass
    # else if request.POST:
    #     pass
    return render(request, 'pages/day-2.html', context)
