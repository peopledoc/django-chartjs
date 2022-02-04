from itertools import islice
from random import randint, shuffle

from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from chartjs.colors import COLORS, next_color
from chartjs.util import date_range, value_or_null
from chartjs.views.columns import BaseColumnsHighChartsView
from chartjs.views.lines import (
    BaseLineChartView,
    BaseLineOptionsChartView,
    HighchartPlotLineChartView,
)
from chartjs.views.pie import HighChartDonutView, HighChartPieView

from demoproject.models import Meter


class ColorsView(TemplateView):
    template_name = "colors.html"

    def get_context_data(self, **kwargs):
        data = super(ColorsView, self).get_context_data(**kwargs)
        data["colors"] = islice(next_color(), 0, 50)
        return data


class ChartMixin(object):
    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_labels(self):
        """Return 7 labels."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_data(self):
        """Return 3 random dataset to plot."""

        def data():
            """Return 7 randint between 0 and 100."""
            return [randint(0, 100) for x in range(7)]

        return [data() for x in range(3)]

    def get_colors(self):
        """Return a new shuffle list of color so we change the color
        each time."""
        colors = COLORS[:]
        shuffle(colors)
        return next_color(colors)


class ColumnHighChartJSONView(ChartMixin, BaseColumnsHighChartsView):
    title = _("Column Highchart test")
    yUnit = "%"
    providers = ["All"]
    credits = {"enabled": False}

    def get_data(self):
        return [super(ColumnHighChartJSONView, self).get_data()]


class LineChartJSONView(ChartMixin, BaseLineChartView):
    pass


class LineHighChartJSONView(ChartMixin, HighchartPlotLineChartView):
    title = _("Line HighChart Test")
    y_axis_title = _("Kangaroos")

    # special - line charts credits are personalized
    credits = {
        "enabled": True,
        "href": "http://example.com",
        "text": "Novapost Team",
    }


class PieHighChartJSONView(ChartMixin, HighChartPieView):
    pass


class DonutHighChartJSONView(ChartMixin, HighChartDonutView):
    pass


class DiscontinuousDatesChartJSONView(ChartMixin, BaseLineChartView):
    start_date = "2019-05-26"
    end_date = "2019-06-04"

    def get_providers(self):
        return ["Water", "Gas"]

    def get_labels(self):
        return [dt for dt in date_range(self.start_date, self.end_date)]

    def get_data(self):
        result = []
        water = Meter.objects.filter(name="water")
        data = [
            item
            for item in value_or_null(
                self.start_date, self.end_date, water, "date", "reading"
            )
        ]
        result.append(data)
        gas = Meter.objects.filter(name="gas")
        data = [
            item
            for item in value_or_null(
                self.start_date, self.end_date, gas, "date", "reading"
            )
        ]
        result.append(data)
        return result


class DiscontinuousDatesHighChartJSONView(ChartMixin, HighchartPlotLineChartView):
    title = _("Discontinuous Line HighChart Test")
    y_axis_title = _("Volume")
    start_date = "2019-05-26"
    end_date = "2019-06-04"

    def get_providers(self):
        return ["Water", "Gas"]

    def get_labels(self):
        return [dt for dt in date_range(self.start_date, self.end_date)]

    def get_data(self):
        result = []
        water = Meter.objects.filter(name="water")
        data = [
            item
            for item in value_or_null(
                self.start_date, self.end_date, water, "date", "reading"
            )
        ]
        result.append(data)
        gas = Meter.objects.filter(name="gas")
        data = [
            item
            for item in value_or_null(
                self.start_date, self.end_date, gas, "date", "reading"
            )
        ]
        result.append(data)
        return result


class LineChartWithOptionsJSONView(ChartMixin, BaseLineOptionsChartView):
    def get_options(self):
        options = {
            "title": {"display": True, "text": "Custom Chart Title"},
            "elements": {"point": {"pointStyle": "rectRounded", "radius": 10}},
            "responsive": False,
        }
        return options


# Pre-configured views.
colors = ColorsView.as_view()

column_highchart_json = ColumnHighChartJSONView.as_view()
line_chart = TemplateView.as_view(template_name="line_chart.html")
line_chart_json = LineChartJSONView.as_view()
line_highchart_json = LineHighChartJSONView.as_view()
pie_highchart_json = PieHighChartJSONView.as_view()
donut_highchart_json = DonutHighChartJSONView.as_view()
discontinuous_dates_chart_json = DiscontinuousDatesChartJSONView.as_view()
discontinuous_dates_highchart_json = DiscontinuousDatesHighChartJSONView.as_view()
line_chart_with_options = LineChartWithOptionsJSONView.as_view()
