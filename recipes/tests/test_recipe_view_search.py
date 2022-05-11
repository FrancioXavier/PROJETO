from django.urls import resolve, reverse
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipesSearchViewsTest(RecipeTestBase):
    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_view_return_404_if_no_search_term(self):
        response = self.client.get(
            reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_terme_is_on_recipe_search_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=Teste'
        response = self.client.get(url)
        self.assertIn(
            'search for &quot;Teste&quot;',
            response.content.decode('utf-8')
        )
