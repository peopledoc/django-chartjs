"""Unit tests for chartjs api."""
import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from demoproject._compat import decode


class LineChartJSTestCase(TestCase):
    def test_line_chartjs(self):
        resp = self.client.get(reverse('line_chart'))
        self.assertContains(resp, 'Chart.min.js')

    def test_list_chartjs_json(self):
        resp = self.client.get(reverse('line_chart_json'))
        try:
            data = json.loads(decode(resp.content))
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
            data = json.loads(decode(resp.content))
        except ValueError:
            self.fail("%r is not valid json" % self.resp.content)
        self.assertIn('title', data)
        self.assertIn('text', data['title'])
        self.assertEqual(data['title']['text'], 'Column Highchart test')
        self.assertIn('credits', data)

    def test_list_chartjs_json(self):
        resp = self.client.get(reverse('line_highchart_json'))
        try:
            data = json.loads(decode(resp.content))
        except ValueError:
            self.fail("%r is not valid json" % self.resp.content)

        self.assertIn('series', data)
        self.assertNotIn('datasets', data)
        self.assertIn('credits', data)

    def test_pie_chartjs_json(self):
        resp = self.client.get(reverse('pie_highchart_json'))
        try:
            json.loads(decode(resp.content))
        except ValueError:
            self.fail("%r is not valid json" % self.resp.content)

    def test_donut_chartjs_json(self):
        resp = self.client.get(reverse('donut_highchart_json'))
        try:
            json.loads(decode(resp.content))
        except ValueError:
            self.fail("%r is not valid json" % self.resp.content)
