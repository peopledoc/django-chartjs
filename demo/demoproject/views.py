# -*- coding: utf-8 -*-
from itertools import islice
from django.views.generic import TemplateView

from chartjs.colors import next_color


class ColorsView(TemplateView):
    template_name = 'colors.html'

    def get_context_data(self, **kwargs):
        data = super(ColorsView, self).get_context_data(**kwargs)
        data['colors'] = islice(next_color(), 0, 50)
        return data

# Pre-configured views.
colors = ColorsView.as_view()
