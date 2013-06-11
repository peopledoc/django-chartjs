# -*- coding: utf-8 -*-
from random import shuffle, randint
from itertools import islice
from django.views.generic import TemplateView

from chartjs.colors import next_color, COLORS
from chartjs.views.lines import BaseLineChartView


class ColorsView(TemplateView):
    template_name = 'colors.html'

    def get_context_data(self, **kwargs):
        data = super(ColorsView, self).get_context_data(**kwargs)
        data['colors'] = islice(next_color(), 0, 50)
        return data


class LineChartJSONView(BaseLineChartView):
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


# Pre-configured views.
colors = ColorsView.as_view()

line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()
