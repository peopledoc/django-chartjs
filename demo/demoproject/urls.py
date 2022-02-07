import django
from django.views.generic import TemplateView
try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path

from pkg_resources import parse_version

from . import views

django_version = parse_version(django.get_version())
if django_version <= parse_version("1.9"):
    from django.conf.urls import patterns

home = TemplateView.as_view(template_name="home.html")

patterns_list = [
    re_path(r"^$", home, name="home"),
    re_path(r"^colors/$", views.colors, name="colors"),
    # Column
    re_path(
        r"^column_highchart/json/$",
        views.column_highchart_json,
        name="column_highchart_json",
    ),
    # Line chart
    re_path(r"^line_chart/$", views.line_chart, name="line_chart"),
    re_path(r"^line_chart/json/$", views.line_chart_json, name="line_chart_json"),
    re_path(
        r"^line_chart/discontinuous/json/$",
        views.discontinuous_dates_chart_json,
        name="discontinuous_line_chart_json",
    ),
    re_path(
        r"^line_chart/options/$",
        views.line_chart_with_options,
        name="line_chart_with_options",
    ),
    re_path(
        r"^line_highchart/json/$", views.line_highchart_json, name="line_highchart_json"
    ),
    re_path(
        r"^line_highchart/discontinuous/json/$",
        views.discontinuous_dates_highchart_json,
        name="discontinuous_line_highchart_json",
    ),
    # Pie
    re_path(r"^pie_highchart/json/$", views.pie_highchart_json, name="pie_highchart_json"),
    re_path(
        r"^donut_highchart/json/$",
        views.donut_highchart_json,
        name="donut_highchart_json",
    ),
]

if django_version <= parse_version("1.9"):
    urlpatterns = patterns("", *patterns_list)
else:
    urlpatterns = patterns_list
