from django.urls import resolve, reverse
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipesCategoryViewsTest(RecipeTestBase):
    def test_recipe_category_templates_loads_recipes(self):
        var_title = 'this is a category title'
        self.make_recipe(title=var_title)
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn(var_title, content)

    def test_recipe_category_view_return_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_template_dont_load_recipe_not_published(self):
        '''test recipe with 'is published' False '''
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:category', args=(1,)))

        self.assertEqual(response.status_code, 404)
