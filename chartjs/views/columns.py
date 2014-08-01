# -*- coding: utf-8 -*-
"""Tools to build Columns HighCharts parameters."""
from . import HighchartsView


class HighchartsColumnView(HighchartsView):
    """Base Class to generate Column HighCharts configuration.

    Define at least title and get_data() to get started.
    """
    chart_type = 'column'
    y_unit = ''

    def get_y_axis(self):
        y_axis = super(HighchartsColumnView, self).get_y_axis()
        y_axis['min'] = getattr(self, 'yMin', 0)
        return y_axis

    def get_y_unit(self):
        # Either change the y_unit attribute or override this method on
        # subclasses to have the y axis unit appear in the tooltip.
        return self.y_unit

    def get_tooltip(self):
        """Return tooltip configuration."""
        return {
            'headerFormat': '''
                <span style="font-size:10px">
                    {point.key}
                 </span>
                 <table>''',
            'pointFormat': '''
                     <tr>
                         <td style="color:{series.color};padding:0">
                             {series.name}:
                         </td>
                         <td style="padding:0">
                             <b>{point.y:.0f} %s</b>
                         </td>
                     </tr>''' % self.get_y_unit(),
            'footerFormat': '</table>',
            'shared': True,
            'useHTML': True
        }

    def get_plot_options(self):
        """Return plotOptions configuration."""
        options = super(HighchartsColumnView, self).get_plot_options()
        options['column'].update({'pointPadding': 0.2, 'borderWidth': 0})
        return options
