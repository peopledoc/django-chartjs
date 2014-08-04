from . import HighchartsView


class HighchartsGaugeView(HighchartsView):
    chart_type = 'gauge'


class HighchartsSolidGaugeView(HighchartsView):
    chart_type = 'solidgauge'
