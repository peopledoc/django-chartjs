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
    zoom_type = None

    def get_title(self):
        """Return graph title."""
        try:
            return self.title
        except AttributeError:  # pragma: no cover
            raise NotImplementedError(  # pragma: no cover
                'You should define self.title or self.get_title')

    def get_subtitle(self):
        return getattr(self, 'subtitle', None)

    def get_providers(self):
        """Return the list of data series names.

        Providers numbers should be equal to series numbers, otherwise there
        may be series in the chart with no name.
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
        data['chart'] = {'type': self.get_type()}
        data['credits'] = self.credits
        data['legend'] = self.get_legend()
        data['plotOptions'] = self.get_plot_options()
        data['series'] = self.get_series()
        data['title'] = {'text': text_type(self.get_title())}
        data['tooltip'] = self.get_tooltip()

        # 'pane' only applies to polar or gauge charts
        if self.polar or self.get_type() in ['gauge', 'solidgauge']:
            data['pane'] = self.get_pane()

        if self.polar:
            data['chart']['polar'] = self.polar,

        if self.zoom_type:
            data['chart']['zoomType'] = self.zoom_type

        subtitle = self.get_subtitle()
        if subtitle is not None:
            data['subtitle'] = {'text': text_type(subtitle)}

        drilldown = self.get_drilldown()
        if drilldown is not None:
            data['drilldown'] = drilldown

        labels = self.get_labels()
        if labels is not None:
            data['labels'] = labels

        x_axis = self.get_x_axis()
        if x_axis is not None:
            data['xAxis'] = x_axis

        y_axis = self.get_y_axis()
        if y_axis is not None:
            data['yAxis'] = y_axis

        return data

    def get_data(self):
        """Return a list of series [[25, 34, 0, 1, 50], ...]).

        In the same order as providers and with the same series length of
        xAxis.
        """
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
        return None

    def get_tooltip(self):
        raise NotImplementedError()

    def get_type(self):
        try:
            return self.chart_type
        except AttributeError:
            raise NotImplementedError()

    def get_labels(self):
        return None

    def get_x_axis(self):
        labels = self.get_labels()
        x_axis = defaultdict(dict)
        if labels is not None:
            x_axis.update(categories=labels)
        return x_axis

    def get_y_axis(self):
        y_axis = defaultdict(dict)
        if self.y_axis_title is not None:
            y_axis.update({
                'title': {
                    'text': text_type(self.y_axis_title),
                }
            })
        return y_axis

    def get_pane(self):
        return defaultdict(dict)
