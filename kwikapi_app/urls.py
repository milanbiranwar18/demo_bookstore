from django.conf.urls import url, include

from . import views
from kwikapi.django import RequestHandler

urlpatterns = [
    url(r'api/', RequestHandler(views.api).handle_request),
]