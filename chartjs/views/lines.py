# -*- coding: utf-8 -*-
"""Tools to build Line charts parameters."""
from six import text_type
from .base import JSONView
from ..colors import next_color
from . import HighchartsView


class BaseLineChartView(JSONView):
    providers = {}

    def get_context_data(self):
        data = {}
        data['datasets'] = self.get_datasets()
        return data

    def get_colors(self):
        return next_color()

    def get_datasets(self):
        datasets = []
        color_generator = self.get_colors()
        data = self.get_data()
        providers = self.get_providers()
        num = len(providers)
        for i, entry in enumerate(data):
            color = tuple(next(color_generator))
            dataset = {'fillColor': "rgba(%d, %d, %d, 0.5)" % color,
                       'strokeColor': "rgba(%d, %d, %d, 1)" % color,
                       'pointColor': "rgba(%d, %d, %d, 1)" % color,
                       'pointStrokeColor': "#fff",
                       'data': entry}
            if i < num:
                dataset['name'] = providers[i]
            datasets.append(dataset)
        return datasets

    def get_labels(self):
        raise NotImplementedError(  # pragma: no cover
            'You should return a labels list. '
            '(i.e: ["January", ...])')

    def get_data(self):
        raise NotImplementedError(  # pragma: no cover
            'You should return a data list list. '
            '(i.e: [[25, 34, 0, 1, 50], ...]).')

    def get_providers(self):
        return []


class HighchartsLineView(HighchartsView):
    chart_type = 'line'
