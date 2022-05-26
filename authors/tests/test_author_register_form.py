from authors.forms import registerForm
from django.test import TestCase
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
        ('username', 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.')  # noqa 501
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
