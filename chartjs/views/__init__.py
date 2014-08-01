# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import izip_longest, takewhile
from six import text_type
from ..colors import next_color
from .base import JSONView


class HighchartsView(JSONView):
    y_axis_title = None
    credits = {'enabled': True}
    polar = False
    stacking = None

    def get_title(self):
        """Return graph title."""
        try:
            return self.title
        except AttributeError:  # pragma: no cover
            raise NotImplementedError(  # pragma: no cover
                'You should define self.title or self.get_title')

    def get_subtitle(self):
        return getattr(self, 'subtitle', '')

    def get_providers(self):
        """Return the list of data series names.

        Providers numbers should be equal to series numbers.
        """
        try:
            return self.providers
        except AttributeError:
            return []

    def get_colors(self):
        return next_color()

    def get_legend(self):
        return defaultdict(dict)

    def get_plot_options(self):
        options = defaultdict(dict)
        if self.stacking:
            options[self.get_type()] = defaultdict(
                dict, {'stacking': self.stacking},
            )
        return options

    def get_context_data(self):
        data = {}
        data['chart'] = {
            'type': self.get_type(),
            'polar': self.polar,
        }

        data['title'] = {
            'text': text_type(self.get_title()),
        }
        data['subtitle'] = {
            'text': text_type(self.get_subtitle()),
        }
        data['plotOptions'] = self.get_plot_options()
        data['legend'] = self.get_legend()
        data['credits'] = self.credits
        data['series'] = self.get_series()
        data['drilldown'] = self.get_drilldown()
        data['tooltip'] = self.get_tooltip()

        labels = self.get_labels()
        if labels:
            data['labels'] = labels

        x_axis = self.get_x_axis()
        if x_axis:
            data['xAxis'] = x_axis

        y_axis = self.get_y_axis()
        if y_axis:
            data['yAxis'] = y_axis

        return data

    def get_data(self):
        raise NotImplementedError(  # pragma: no cover
            'You should return a data list list. '
            '(i.e: [[25, 34, 0, 1, 50], ...]).')

    def get_series(self):
        series = []
        # izip_longest rather than zip because get_providers and get_colors
        # might be shorter than get_data (or completely empty)
        zipped = izip_longest(
            self.get_data(),
            self.get_providers(),
            self.get_colors(),
        )

        # Loop through data, names & colors for as long as we have data
        # (get_colors might return a generator that produces values
        # indefinitely)
        for datum, name, color in takewhile(lambda x: x[0], zipped):
            serie = {'data': datum}
            if name:
                serie['name'] = name
            if color:
                serie['color'] = "rgba(%d, %d, %d, 1)" % tuple(color)
            series.append(serie)

        return series

    def get_drilldown(self):
        return []

    def get_tooltip(self):
        raise NotImplementedError()

    def get_type(self):
        try:
            return self.chart_type
        except AttributeError:
            raise NotImplementedError()

    def get_labels(self):
        return []

    def get_x_axis(self):
        return {'categories': self.get_labels()}

    def get_y_axis(self):
        return None
