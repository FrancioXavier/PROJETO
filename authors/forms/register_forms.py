from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password


class registerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Your first name')
        add_placeholder(self.fields['last_name'], 'Your last name')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    first_name = forms.CharField(
        error_messages={'required': 'write your first name'},
        label='First name'
    )
    last_name = forms.CharField(
        error_messages={'required': 'write your last name'},
        label='Last name'
    )
    email = forms.EmailField(
        error_messages={'required': 'write your e-mail'},
        label='E-mail',
        help_text='The email must be valid.'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'password must not be empty'
        },
        help_text=(
            'password must have one uppercase letter, one '
            'lower case letter, and a number'
        ),
        validators=[strong_password],
        label='Password'
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Repeat the password',
        error_messages={
            'required': 'password2 must not be empty'
        },
    )
    username = forms.CharField(
        label='Username',
        help_text='Username must have letters, numbers or one of those @.+-_. '  # noqa 501
        'the lenght should be between 4 and 50 characters.',
        error_messages={
            'required': 'This field must not be empty.',
            'min_length': 'This field must have at least 4 characters',
            'max_length': 'This field must have less or equal 50 characters'
        },
        min_length=4, max_length=50,
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

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password2 must be equal',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User email is already in use',
                code='invalid'
            )

        return email
