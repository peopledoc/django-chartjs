###############
Django Chart.js
###############

Django Chart.js lets you manage charts in you Django application.

Using a set of predefined Class Based Views your are able to get
started after writting just your SQL query.

* Authors: Rémy Hubscher and `contributors
  <https://github.com/novagile/django-chartjs/graphs/contributors>`_
* Licence: BSD
* Compatibility: Django 1.5+, python2.7 up to python3.3
* Project URL: https://github.com/novagile/django-i18nurl


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
    	</head>
    	<body>
            <h1>Some Line Charts loaded in Ajax!</h1>
            
            <canvas id="myChart" width="500" height="400"></canvas>
    
            <script type="text/javascript" src="http://code.jquery.com/jquery-1.10.0.min.js"></script>
            <script type="text/javascript" src="{% static 'js/Chart.min.js' %}"></script>
            <script type="text/javascript">
                $.get('{% url 'line_chart_json' %}', function(data) {
                    var ctx = $("#myChart").get(0).getContext("2d");
                    new Chart(ctx).Line(data);
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
            """Return 7 labels."""
            return ["January", "February", "March", "April", "May", "June", "July"]
    
        def get_data(self):
            """Return 3 random dataset to plot."""
            def data():
                """Return 7 randint between 0 and 100."""
                return [randint(0, 100) for x in range(7)]
    
            return [data() for x in range(3)]
    
    
    line_chart = TemplateView.as_view(template_name='line_chart.html')
    line_chart_json = LineChartJSONView.as_view()


3. Get a Chart.js Line Chart
++++++++++++++++++++++++++++

.. image:: https://raw.github.com/novagile/django-chartjs/master/docs/_static/django-chartjs.png


It is that simple!

For other example, don't hesitate to look at the demo project.

Also contribute your demo!
