from django.conf.urls import url
from .api import *

urlpatterns = [
    url(r'^events/$', EventList.as_view(), name='events'),
    url(r'^events/(?P<event_id>\d+)/$', EventDetails.as_view(), name='event'),
    url(r'^events/(?P<event_id>\d+)/signups/$', EventSignUp.as_view(), name='event-signups'),
    url(r'^events/(?P<event_id>\d+)/signups/(?P<signup_id>\d+)/$', SignUpDetails.as_view(), name='event-signup'),
    url(r'^user/$', UserDetails.as_view(), name='user'),
    url(r'^user/register$', UserCreate.as_view(), name='user-register'),
    url(r'^user/signup-event/(?P<event_id>\d+)/$', UserSignUpDetails.as_view(), name='user-signup'),
]
