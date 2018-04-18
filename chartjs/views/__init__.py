# -*- coding: utf-8 -*-
from six import text_type
from ..colors import next_color
from .base import JSONView


class HighChartsView(JSONView):
    title = None
    y_axis_title = None
    credits = {'enabled': True}

    def get_colors(self):
        return next_color()

    def get_legend(self):
        return {}

    def get_plot_options(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super(HighChartsView, self).get_context_data(**kwargs)
        context.update({
            'title': {'text': text_type(self.title)},
            'plotOptions': self.get_plot_options(),
            'legend': self.get_legend(),
            'credits': self.credits,
            })
        return context

    def get_data(self):
        raise NotImplementedError(  # pragma: no cover
            'You should return a data list list. '
            '(i.e: [[25, 34, 0, 1, 50], ...]).')

    def get_series(self):
        series = []
        color_generator = self.get_colors()
        data = self.get_data()
        providers = self.get_providers()
        num = len(providers)
        for i, data in enumerate(self.get_data()):
            color = tuple(next(color_generator))
            serie = {
                'color': "rgba(%d, %d, %d, 1)" % color,
                'data': data
            }
            if i < num:
                serie['name'] = providers[i]
            series.append(serie)
        return series
