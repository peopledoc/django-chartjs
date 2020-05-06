"""Tools to build Line charts parameters."""
from . import HighChartsView
from ..colors import next_color
from .base import JSONView


class BaseLineChartView(JSONView):
    providers = {}

    def get_context_data(self, **kwargs):
        context = super(BaseLineChartView, self).get_context_data(**kwargs)
        context.update({"labels": self.get_labels(), "datasets": self.get_datasets()})
        return context

    def get_colors(self):
        return next_color()

    def get_dataset_options(self, index, color):
        default_opt = {
            "backgroundColor": "rgba(%d, %d, %d, 0.5)" % color,
            "borderColor": "rgba(%d, %d, %d, 1)" % color,
            "pointBackgroundColor": "rgba(%d, %d, %d, 1)" % color,
            "pointBorderColor": "#fff",
        }
        return default_opt

    def get_datasets(self):
        datasets = []
        color_generator = self.get_colors()
        data = self.get_data()
        providers = self.get_providers()
        num = len(providers)
        for i, entry in enumerate(data):
            color = tuple(next(color_generator))
            dataset = {"data": entry}
            dataset.update(self.get_dataset_options(i, color))
            if i < num:
                dataset["label"] = providers[i]  # series labels for Chart.js
                dataset["name"] = providers[i]  # HighCharts may need this
            datasets.append(dataset)
        return datasets

    def get_labels(self):
        raise NotImplementedError(  # pragma: no cover
            "You should return a labels list. " '(i.e: ["January", ...])'
        )

    def get_data(self):
        raise NotImplementedError(  # pragma: no cover
            "You should return a data list list. " "(i.e: [[25, 34, 0, 1, 50], ...])."
        )

    def get_providers(self):
        return []


class BaseLineOptionsChartView(BaseLineChartView):
    def get_context_data(self, **kwargs):
        context = super(BaseLineChartView, self).get_context_data(**kwargs)
        context.update(
            {
                "data": {"labels": self.get_labels(), "datasets": self.get_datasets()},
                "options": self.get_options(),
            }
        )
        return context

    def get_options(self):
        raise NotImplementedError(  # pragma: no cover
            "You should return a dict. " '(i.e.: {"responsive": false})'
        )


class HighchartPlotLineChartView(HighChartsView):
    y_axis_title = None

    def get_y_axis_options(self):
        return {"title": {"text": u"%s" % self.y_axis_title}}

    def get_x_axis_options(self):
        return {"categories": self.get_labels()}

    def get_context_data(self, **kwargs):
        data = super(HighchartPlotLineChartView, self).get_context_data(**kwargs)
        data.update(
            {
                "labels": self.get_labels(),
                "xAxis": self.get_x_axis_options(),
                "series": self.get_series(),
                "yAxis": self.get_y_axis_options(),
            }
        )
        return data

    def get_providers(self):
        return []
