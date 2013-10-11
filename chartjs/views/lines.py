# -*- coding: utf-8 -*-
"""Tools to build Line charts parameters."""
from .base import JSONView
from ..colors import next_color


class BaseLineChartView(JSONView):
    providers = {}

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
        data = self.get_data()
        providers = self.get_providers()
        num = len(providers)
        for i, data in enumerate(self.get_data()):
            color = tuple(next(color_generator))
            dataset = {'fillColor': "rgba(%d, %d, %d, 0.5)" % color,
                       'strokeColor': "rgba(%d, %d, %d, 1)" % color,
                       'pointColor': "rgba(%d, %d, %d, 1)" % color,
                       'pointStrokeColor': "#fff",
                       'data': data}
            if i < num:
                dataset['name'] = providers[i]
            datasets.append(dataset)
        return datasets

    def get_labels(self):
        raise NotImplementedError(
            'You should return a labels list. '
            '(i.e: ["January", ...])')

    def get_data(self):
        raise NotImplementedError(
            'You should return a data list list. '
            '(i.e: [[25, 34, 0, 1, 50], ...]).')

    def get_providers(self):
        return []


class HighchartPlotLineChartView(BaseLineChartView):
    title = None
    y_axis_title = None

    def get_context_data(self):
        data = {}
        data['labels'] = self.get_labels()
        data['series'] = self.get_series()
        data['title'] = {'title': self.title}
        data['yAxis'] = {'title': {'text': u'%s' % self.y_axis_title}}
        return data

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
