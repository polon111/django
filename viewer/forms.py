from django.forms import (
    ModelForm, CharField, IntegerField,
)
from viewer.models import Movie
from viewer.validators import PastMonthField, capitalized_validator

from django.core.exceptions import ValidationError

import re


class MovieForm(ModelForm):
    class Meta: #subklasa opisująca dane z których będzie tworzony form
        model = Movie #model na podstawie tworzy formularz
        fields = '__all__' #wykorzystujemy wszystkie pola z modelu

    #pola z własnymi walidatorami dodajemy oddzielnie poza META
    title = CharField(validators=[capitalized_validator])
    rating = IntegerField(min_value=1, max_value=10)
    released = PastMonthField()

    def clean_description(self):
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)


    def clean(self):
        result = super().clean()
        if result['genre'].name == 'comedy' and result['rating'] > 7:
            self.add_error('genre', '')
            self.add_error('rating', '')
            raise ValidationError(
                'Commedies aren\'t so good to be over 7'
            )
        return result
