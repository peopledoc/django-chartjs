#-*- coding: utf-8 -*-
from six import text_type
from ..colors import next_color
from .base import JSONView


class HighchartsView(JSONView):
    title = None
    y_axis_title = None
    credits = {'enabled': True}

    def get_title(self):
        """Return graph title."""
        try:
            return self.title
        except AttributeError:  # pragma: no cover
            raise NotImplementedError(  # pragma: no cover
                'You should define self.title or self.get_title')

    def get_colors(self):
        return next_color()

    def get_legend(self):
        return {}

    def get_plot_options(self):
        return {}

    def get_context_data(self):
        data = {}
        data['title'] = {'text': text_type(self.get_title())}
        data['plotOptions'] = self.get_plot_options()
        data['legend'] = self.get_legend()
        data['credits'] = self.credits
        data['series'] = self.get_series()
        data['drilldown'] = self.get_drilldown()
        return data

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

    def get_drilldown(self):
        return []
