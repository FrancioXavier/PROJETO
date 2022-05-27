from unittest import TestCase

from authors.forms import registerForm
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Your first name'),
        ('last_name', 'Your last name'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_placeholder_is_correct(self, field, placeholder):
        form = registerForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('password', 'password must have one uppercase letter, one '
         'lower case letter, and a number'),
        ('email', 'The email must be valid.'),
        ('username',
                    'Username must have letters, numbers or one of those @.+-_. '  # noqa 501
                    'the lenght should be between 4 and 50 characters.')
    ])
    def test_help_text_is_correct(self, field, needed):
        form = registerForm()
        help_text = form[field].field.help_text
        self.assertEqual(help_text, needed)

    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('password', 'Password'),
        ('password2', 'Repeat the password'),
    ])
    def test_label_is_correct(self, field, needed):
        form = registerForm()
        label = form[field].field.label
        self.assertEqual(label, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@any.com',
            'password': 'Password1',
            'password2': 'Password1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty.'),
        ('password', 'password must not be empty'),
        ('password2', 'password2 must not be empty'),
        ('first_name', 'write your first name'),
        ('last_name', 'write your last name'),
        ('email', 'write your e-mail'),

    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_is_in_min_lenght(self):
        self.form_data['username'] = 'aaa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'This field must have at least 4 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_is_in_max_lenght(self):
        self.form_data['username'] = 'a'*51
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'This field must have less or equal 50 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
