"""tech_kaushalya URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import pages.views as pages_views
import forms.views as forms_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pages_views.home_view, name='home'),
    path('schedule/<int:day>/', pages_views.schedule_view, name='schedule'),
    path('updates_submit/', forms_views.updates_submit_view,
         name='updates_submit'),
    path('register/<int:event_id>/', forms_views.register_view,
         name='register')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
