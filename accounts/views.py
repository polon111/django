from django.shortcuts import render

# Create your views here.

from django.contrib.auth.views import LoginView


class SubmittableLoginView(LoginView):
    template_name = 'form.html'
