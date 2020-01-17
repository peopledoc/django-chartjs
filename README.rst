##############
Django Chartjs
##############

Django Chartjs lets you manage charts in your Django application.

.. image:: https://travis-ci.org/peopledoc/django-chartjs.svg?branch=master
   :target: https://travis-ci.org/peopledoc/django-chartjs
.. image:: https://coveralls.io/repos/peopledoc/django-chartjs/badge.png?branch=master&style=flat
   :target: https://coveralls.io/r/peopledoc/django-chartjs?branch=master
.. image:: https://img.shields.io/pypi/v/django-chartjs.svg
   :target: https://pypi.python.org/pypi/django-chartjs/


This is compatible with Chart.js and Highcharts JS libraries.

Using a set of predefined Class Based Views you are able to get
started after writing just your SQL query.

* Authors: Rémy Hubscher and `contributors
  <https://github.com/peopledoc/django-chartjs/graphs/contributors>`_
* Licence: BSD
* Compatibility: Django 1.10, 2.2 and 3.0, python3.6 up to python3.8
* Project URL: https://github.com/peopledoc/django-chartjs


Getting Started
===============

Install django-chartjs::

    pip install django-chartjs


Add it to your ``INSTALLED_APPS`` settings::

    INSTALLED_APPS = (
        '...',
        'chartjs',
    )


Using it
========

A simple Line Chart example.

1. Create the HTML file
+++++++++++++++++++++++

.. code-block:: html

    {% load staticfiles %}
    <html>
        <head>
            <title>django-chartjs line chart demo</title>
            <!--[if lte IE 8]>
                <script src="{% static 'js/excanvas.js' %}"></script>
            <![endif]-->
        </head>
        <body>
            <h1>Some Line Charts loaded in Ajax!</h1>
            
            <canvas id="myChart" width="500" height="400"></canvas>
    
            <script type="text/javascript" src="http://code.jquery.com/jquery-1.10.0.min.js"></script>
            <script type="text/javascript" src="{% static 'js/Chart.min.js' %}"></script>
            <script type="text/javascript">
                $.get('{% url "line_chart_json" %}', function(data) {
                    var ctx = $("#myChart").get(0).getContext("2d");
                    new Chart(ctx, {
                        type: 'line', data: data
                    });
                });
            </script>
        </body>
    </html>


2. Create the view with labels and data definition
++++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: python

    from random import randint
    from django.views.generic import TemplateView
    from chartjs.views.lines import BaseLineChartView
    
    
    class LineChartJSONView(BaseLineChartView):
        def get_labels(self):
            """Return 7 labels for the x-axis."""
            return ["January", "February", "March", "April", "May", "June", "July"]

        def get_providers(self):
            """Return names of datasets."""
            return ["Central", "Eastside", "Westside"]

        def get_data(self):
            """Return 3 datasets to plot."""
    
            return [[75, 44, 92, 11, 44, 95, 35],
                    [41, 92, 18, 3, 73, 87, 92],
                    [87, 21, 94, 3, 90, 13, 65]]
    
    
    line_chart = TemplateView.as_view(template_name='line_chart.html')
    line_chart_json = LineChartJSONView.as_view()


3. Get a Chart.js Line Chart
++++++++++++++++++++++++++++

.. image:: https://raw.github.com/peopledoc/django-chartjs/master/docs/_static/django-chartjs.png


It is that simple!

For other examples including a HighCharts line chart, don't hesitate to look at the demo project.

Also, feel free to contribute your demo!
