from django.urls import re_path
from .api import *

urlpatterns = [
    re_path(r'^events/$', EventList.as_view(), name='events'),
    re_path(r'^events/(?P<event_id>\d+)/$', EventDetails.as_view(), name='event'),
    re_path(r'^events/(?P<event_id>\d+)/signups/$', EventSignUp.as_view(), name='event-signups'),
    re_path(r'^events/(?P<event_id>\d+)/signups/(?P<signup_id>\d+)/$', SignUpDetails.as_view(), name='event-signup'),
    re_path(r'^user/$', UserDetails.as_view(), name='user'),
    re_path(r'^user/register$', UserCreate.as_view(), name='user-register'),
    re_path(r'^user/signup-event/(?P<event_id>\d+)/$', UserSignUpDetails.as_view(), name='user-signup'),
]
