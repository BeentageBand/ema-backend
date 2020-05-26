"""restserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from ema.api import EventList, EventDetails, EventSignup, SignUpDetails

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/events/$', EventList.as_view(), name='events'),
    url(r'^api/events/(?P<event_id>\d+)/$', EventDetails.as_view(), name='events'),
    url(r'^api/events/(?P<event_id>\d+)/signups/$', EventSignup.as_view(), name='signups'),
    url(r'^api/events/(?P<event_id>\d+)/signups/(?P<signup_id>\d+)/$', SignUpDetails.as_view(), name='signups'),
]
