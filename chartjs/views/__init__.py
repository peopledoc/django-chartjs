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
