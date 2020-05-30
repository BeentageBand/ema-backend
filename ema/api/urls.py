from django.conf.urls import url
from .api import EventList, EventDetails, EventSignup, SignUpDetails

urlpatterns = [
    url(r'^events/$', EventList.as_view(), name='events'),
    url(r'^events/(?P<event_id>\d+)/$', EventDetails.as_view(), name='events'),
    url(r'^events/(?P<event_id>\d+)/signups/$', EventSignup.as_view(), name='signups'),
    url(r'^events/(?P<event_id>\d+)/signups/(?P<signup_id>\d+)/$', SignUpDetails.as_view(), name='signups'),
]
