from ..colors import next_color
from .base import JSONView


class HighChartsView(JSONView):
    title = None
    y_axis_title = None

    def get_colors(self):
        return next_color()

    def get_context_data(self):
        data = {}
        data['title'] = {'text': self.title}
        return data

    def get_data(self):
        raise NotImplementedError(
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
