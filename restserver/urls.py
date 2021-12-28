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
from django.urls import re_path, path
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.views.generic.base import RedirectView

schema_view = get_schema_view(
    openapi.Info(
        title="Event Manager Application (EMA) API",
        default_version='v1',
        description="EMA API Snippets",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('ema.api.urls')),
    re_path(r'^doc/$', schema_view.with_ui('redoc', cache_timeout=0), name='doc'),
    re_path(r'^accounts/profile/$', RedirectView.as_view(pattern_name='user'), name='redirect-user'),
    re_path(r'^.*$', RedirectView.as_view(pattern_name='doc'), name='redirect-doc'),
]
