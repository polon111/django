from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from viewer.models import Movie
from viewer.forms import MovieForm
from django.urls import reverse_lazy
from django.shortcuts import render
import datetime

from logging import getLogger
LOGGER = getLogger()

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

class SubmittableLoginView(LoginView):
    template_name = 'form.html'

@login_required
def generate_demo(request): # <=== ZMIANA
    our_get = request.GET.get('name', '')
    return render(
        request, template_name='demo.html',
        context={'our_get': our_get,
                 'list': ['pierwszy', 'drugi', 'trzeci', 'czwarty'],
                 'nasza_data': datetime.datetime.now()
                 }
    )


class MoviesView(LoginRequiredMixin, ListView):
    template_name = 'movies.html'
    model = Movie


class MovieCreateView(LoginRequiredMixin, CreateView):
    template_name = 'formAddEditMovie.html'
    form_class = MovieForm
    success_url = reverse_lazy('movie_create')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data')
        return super().form_invalid(form)


class MovieUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'formAddEditMovie.html'
    form_class = MovieForm
    # adres pobrany z URLs na który zostaniemy przekierowani
    success_url = reverse_lazy('index')
    model = Movie

    def from_invalid(self, form):
        # odkładamy w logach informacje o operacji
        LOGGER.warning('User provided invalid data when updating')
        # zwracamy wynik działaniapierwotnej funkcji form_invalid
        return super().form_invalid(form)

class MovieDeleteView(LoginRequiredMixin, DeleteView):
    # Nazwa szablonu wraz z rozszerzeniem którą pobieramy z folderu templates
    template_name = 'delete_movie.html'
    success_url = reverse_lazy('index')
    #Nazwa encji, z której będziemy
    model = Movie