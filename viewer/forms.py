from django.forms import (
    Form, CharField, ModelChoiceField, IntegerField, DateField, Textarea
)
from viewer.models import Genre
from viewer.validators import PastMonthField, capitalized_validator
from django.core.exceptions import ValidationError

import re


class MovieForm(Form):
    title = CharField(max_length=128)
    genre = ModelChoiceField(queryset=Genre.objects)
    rating = IntegerField(min_value=1, max_value=10)
    released = PastMonthField()
    description = CharField(widget=Textarea, required=False)

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
