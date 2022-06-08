from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2'),

        self._my_errors = defaultdict(list)

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            'cover',
            'category',
        ]
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        preparation_steps = cleaned_data.get('preparation_steps')

        if len(title) < 5:
            self._my_errors['title'].append(
                'The title must have at least 5 characters.')

        if len(description) < 10:
            self._my_errors['description'].append(
                'The description must have at least 10 characters.')

        if len(preparation_steps) < 10:
            self._my_errors['preparation_steps'].append(
                'The preparation steps must have at least 10 characters.')

        if title == description:
            self._my_errors['title'].append(
                'Can not be the same as description.')
            self._my_errors['description'].append(
                'Can not be the same as title.')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_preparation_time(self):
        fied_name = 'preparation_time'
        field_value = self.cleaned_data.get(fied_name)

        if not is_positive_number(field_value):
            self._my_errors[fied_name].append('The number must be positive.')

        return field_value

    def clean_servings(self):
        fied_name = 'servings'
        field_value = self.cleaned_data.get(fied_name)

        if not is_positive_number(field_value):
            self._my_errors[fied_name].append('The number must be positive.')

        return field_value
