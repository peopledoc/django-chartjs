from django.conf.urls import patterns, url

from .views import colors


urlpatterns = patterns(
    '',
    url(r'^$', colors, name='colors'),
)
