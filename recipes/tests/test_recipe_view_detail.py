from django.urls import resolve, reverse
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipesDetailViewsTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_return_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 100}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_templates_loads_recipes(self):
        var_title = 'this is a detail page - it loads just one recipe'
        self.make_recipe(title=var_title)

        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={
                    'id': 1
                }
            )
        )
        content = response.content.decode('utf-8')
        self.assertIn(var_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        '''test recipe with 'is published' False '''
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={
                    'id': recipe.id
                }
            )
        )

        self.assertEqual(response.status_code, 404)
