"""Tools to build Columns HighCharts parameters."""
from .base import JSONView


class BaseColumnsHighChartsView(JSONView):
    """Base Class to generate Column HighCharts configuration.

    Define at least title, yUnit, providers, get_labels() and
    get_data() to get started.
    """

    providers = {}
    credits = {"enabled": True}

    def get_context_data(self, **kwargs):
        """Return graph configuration."""
        context = super(BaseColumnsHighChartsView, self).get_context_data(**kwargs)
        context.update(
            {
                "chart": self.get_type(),
                "title": self.get_title(),
                "subtitle": self.get_subtitle(),
                "xAxis": self.get_xAxis(),
                "yAxis": self.get_yAxis(),
                "tooltip": self.get_tooltip(),
                "plotOptions": self.get_plotOptions(),
                "series": self.get_series(),
                "credits": self.credits,
            }
        )
        return context

    def get_type(self):
        """Return graph type."""
        return {"type": "column"}

    def get_title(self):
        """Return graph title."""
        try:
            return {"text": u"%s" % self.title}
        except AttributeError:  # pragma: no cover
            raise NotImplementedError(  # pragma: no cover
                "You should define self.title or self.get_title"
            )

    def get_subtitle(self):
        """Return graph subtitle."""
        subtitle = u"%s" % getattr(self, "subtitle", "")
        return subtitle

    def get_xAxis(self):
        return {"categories": self.get_labels()}

    def get_labels(self):
        raise NotImplementedError(  # pragma: no cover
            "You should return a labels list. " '(i.e: ["January", ...])'
        )

    def get_yAxis(self):
        return {"min": getattr(self, "yMin", 0), "title": self.get_yTitle()}

    def get_yTitle(self):
        """Return yAxis title."""
        subtitle = u"%s" % getattr(self, "subtitle", "")
        return subtitle

    def get_yUnit(self):
        try:
            return self.yUnit
        except AttributeError:  # pragma: no cover
            raise NotImplementedError(  # pragma: no cover
                "Please define the yAxis unit (self.yUnit)."
            )

    def get_tooltip(self):
        """Return tooltip configuration."""
        return {
            "headerFormat": """
                <span style="font-size:10px">
                    {point.key}
                 </span>
                 <table>""",
            "pointFormat": """
                     <tr>
                         <td style="color:{series.color};padding:0">
                             {series.name}:
                         </td>
                         <td style="padding:0">
                             <b>{point.y:.0f} %s</b>
                         </td>
                     </tr>"""
            % self.get_yUnit(),
            "footerFormat": "</table>",
            "shared": True,
            "useHTML": True,
        }

    def get_plotOptions(self):
        """Return plotOptions configuration."""
        return {"column": {"pointPadding": 0.2, "borderWidth": 0}}

    def get_series(self):
        """Generate HighCharts series from providers and data."""
        series = []
        data = self.get_data()
        providers = self.get_providers()
        for i, d in enumerate(data):
            series.append({"name": providers[i], "data": d})
        return series

    def get_data(self):
        """Return a list of series [[25, 34, 0, 1, 50], ...]).

        In the same order as providers and with the same serie length
        of xAxis.
        """
        raise NotImplementedError(  # pragma: no cover
            "You should return a data list list. " "(i.e: [[25, 34, 0, 1, 50], ...])."
        )

    def get_providers(self):
        """Return the list of data series names.

        Providers numbers should be equal to series numbers.
        """
        try:
            return self.providers
        except AttributeError:  # pragma: no cover
            raise NotImplementedError(  # pragma: no cover
                "You should define self.providers of self.get_providers."
            )
