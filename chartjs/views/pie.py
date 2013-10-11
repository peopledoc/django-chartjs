from . import HighChartsView


class HighChartPieView(HighChartsView):

    def get_context_data(self):
        data = super(HighChartPieView, self).get_context_data()
        data['series'] = self.get_series()
        return data

    def get_series(self):
        series = super(HighChartPieView, self).get_series()
        for serie in series:
            serie.update({'type': 'pie'})
        return series

    def get_providers(self):
        return []
