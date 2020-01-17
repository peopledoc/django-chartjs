from . import HighChartsView


class HighChartPieView(HighChartsView):
    def get_context_data(self, **kwargs):
        data = super(HighChartPieView, self).get_context_data(**kwargs)
        data["series"] = self.get_series()
        return data

    def get_series(self):
        series = super(HighChartPieView, self).get_series()
        for serie in series:
            serie.update({"type": "pie"})
        return series

    def get_providers(self):
        return []


class HighChartDonutView(HighChartPieView):
    inner_size = "50%"

    def get_series(self):
        series = super(HighChartDonutView, self).get_series()
        for serie in series:
            serie.update({"innerSize": self.inner_size})
        return series

    def get_plot_options(self):
        options = super(HighChartDonutView, self).get_plot_options()
        options.update({"pie": {"showInLegend": True}})
        return options
