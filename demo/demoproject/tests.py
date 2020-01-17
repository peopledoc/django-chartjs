"""Unit tests for chartjs api."""
import json

from django.test import TestCase
try:
    from django.urls import reverse
except ImportError:
    # remove import shim when support for django 1.9 is dropped
    from django.core.urlresolvers import reverse

from demoproject.models import Meter
from chartjs.util import value_or_null, NULL


class LineChartJSTestCase(TestCase):
    def test_line_chartjs(self):
        resp = self.client.get(reverse('line_chart'))
        self.assertContains(resp, 'Chart.min.js')

    def test_list_chartjs_json(self):
        resp = self.client.get(reverse('line_chart_json'))
        try:
            data = json.loads(resp.content.decode('utf-8'))
        except ValueError:
            self.fail("%r is not valid json" % self.resp.content)

        self.assertIn('datasets', data)
        self.assertNotIn('series', data)


class ColorTestCase(TestCase):
    def test_colorview(self):
        resp = self.client.get(reverse('colors'))
        self.assertContains(resp, '100px')


class HighChartJSTestCase(TestCase):

    def test_column_chartjs_json(self):
        resp = self.client.get(reverse('column_highchart_json'))
        try:
            data = json.loads(resp.content.decode("utf-8"))
        except ValueError:
            self.fail("%r is not valid json" % self.resp.content)
        self.assertIn('title', data)
        self.assertIn('text', data['title'])
        self.assertEqual(data['title']['text'], 'Column Highchart test')
        self.assertIn('credits', data)
        credits = data['credits']
        self.assertEqual(credits['enabled'], False)

    def test_list_chartjs_json(self):
        resp = self.client.get(reverse('line_highchart_json'))
        try:
            data = json.loads(resp.content.decode("utf-8"))
        except ValueError:
            self.fail("%r is not valid json" % self.resp.content)

        self.assertIn('series', data)
        self.assertNotIn('datasets', data)
        self.assertIn('credits', data)
        credits = data['credits']
        self.assertEqual(credits['enabled'], True)
        self.assertEqual(credits['href'], 'http://example.com')
        self.assertEqual(credits['text'], 'Novapost Team')

    def test_pie_chartjs_json(self):
        resp = self.client.get(reverse('pie_highchart_json'))
        try:
            json.loads(resp.content.decode("utf-8"))
        except ValueError:
            self.fail("%r is not valid json" % self.resp.content)

    def test_donut_chartjs_json(self):
        resp = self.client.get(reverse('donut_highchart_json'))
        try:
            json.loads(resp.content.decode("utf-8"))
        except ValueError:
            self.fail("%r is not valid json" % self.resp.content)


class DiscontinuousDataTestCase(TestCase):

    def setUp(self):
        self.start_date = "2019-05-26"
        self.end_date = "2019-06-04"
        # water meter readings
        Meter.objects.create(date="2019-05-26", name="water", reading=10)
        Meter.objects.create(date="2019-05-27", name="water", reading=12)
        Meter.objects.create(date="2019-05-28", name="water", reading=13)
        Meter.objects.create(date="2019-05-29", name="water", reading=15)
        Meter.objects.create(date="2019-06-01", name="water", reading=16)
        Meter.objects.create(date="2019-06-02", name="water", reading=18)
        Meter.objects.create(date="2019-06-03", name="water", reading=20)
        Meter.objects.create(date="2019-06-04", name="water", reading=21)
        # gas meter readings
        Meter.objects.create(date="2019-05-28", name="gas", reading=15)
        Meter.objects.create(date="2019-05-29", name="gas", reading=13)
        Meter.objects.create(date="2019-05-30", name="gas", reading=12)
        Meter.objects.create(date="2019-05-31", name="gas", reading=14)
        Meter.objects.create(date="2019-06-01", name="gas", reading=16)
        Meter.objects.create(date="2019-06-02", name="gas", reading=17)

    def test_generator_fills_end_values_with_null(self):
        queryset = Meter.objects.filter(name="gas")
        actual_data = []
        for item in value_or_null(self.start_date, self.end_date, queryset, "date", "reading"):
            actual_data.append(item)
        expected_data = [NULL, NULL, 15, 13, 12, 14, 16, 17, NULL, NULL]
        self.assertEqual(actual_data, expected_data)

    def test_generator_fills_middle_values_with_null(self):
        queryset = Meter.objects.filter(name="water")
        actual_data = []
        for item in value_or_null(self.start_date, self.end_date, queryset, "date", "reading"):
            actual_data.append(item)
        expected_data = [10, 12, 13, 15, NULL, NULL, 16, 18, 20, 21]
        self.assertEqual(actual_data, expected_data)


class ChartOptionsTestCase(TestCase):
    def test_line_chart_with_options_json(self):
        resp = self.client.get(reverse('line_chart_with_options'))
        try:
            data = json.loads(resp.content.decode("utf-8"))
        except ValueError:
            self.fail("%r is not valid json" % self.resp.content)
        self.assertIn('data', data)
        self.assertIn('datasets', data['data'])
        self.assertIn('labels', data['data'])
        self.assertIn('options', data)
        self.assertIn('title', data['options'])
