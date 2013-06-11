# -*- coding: utf-8 -*-
"""Tools to build Line charts parameters."""
from .base import JSONView
from ..colors import next_color


class BaseLineChartView(JSONView):
    def get_context_data(self):
        data = {}
        data['labels'] = self.get_labels()
        data['datasets'] = self.get_datasets()
        return data

    def get_colors(self):
        return next_color()

    def get_datasets(self):
        datasets = []
        color_generator = self.get_colors()
        for data in self.get_data():
            color = tuple(next(color_generator))
            datasets.append({'fillColor': "rgba(%d, %d, %d, 0.5)" % color,
                             'strokeColor': "rgba(%d, %d, %d, 1)" % color,
                             'pointColor': "rgba(%d, %d, %d, 1)" % color,
                             'pointStrokeColor': "#fff",
                             'data': data})
        return datasets

    def get_labels(self):
        raise NotImplementedError(
            'You should return a labels list. '
            '(i.e: ["January", ...])')

    def get_data(self):
        raise NotImplementedError(
            'You should return a data list list. '
            '(i.e: [[25, 34, 0, 1, 50], ...]).')
