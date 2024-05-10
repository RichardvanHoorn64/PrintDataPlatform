from django.shortcuts import render
from datetime import datetime, timedelta
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin


class CreateNewPaperSpec(TemplateView, LoginRequiredMixin):
    template_name = 'homepage/conditions.html'
