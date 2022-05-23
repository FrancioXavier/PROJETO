from django import forms
from django.contrib.auth.models import User


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class registerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Your first name')
        add_placeholder(self.fields['last_name'], 'Your last name')

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'password must not be empty'
        },
        help_text=(
            'password must have one uppercase letter, one '
            'lower case letter, and a number'
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        }),
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
            'email',

        ]

        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'password': 'Password',
            'email': 'E-mail',
        }

        help_texts = {
            'email': 'The email must be valid.'
        }

        error_messages = {
            'username': {
                'required': 'This field must be empty.'
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name (duh)'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password'
            }),
        }
