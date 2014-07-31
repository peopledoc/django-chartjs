from . import HighchartsView


class HighchartsPieView(HighchartsView):
    chart_type = 'pie'

    def get_series(self):
        series = super(HighchartsPieView, self).get_series()
        for serie in series:
            serie.update({'type': 'pie'})
        return series

    def get_providers(self):
        return []


class HighchartsDonutView(HighchartsPieView):
    inner_size = '50%'

    def get_series(self):
        series = super(HighchartsDonutView, self).get_series()
        for serie in series:
            serie.update({"innerSize": self.inner_size})
        return series

    def get_plot_options(self):
        options = super(HighchartsDonutView, self).get_plot_options()
        options.update({'pie': {"showInLegend": True}})
        return options
