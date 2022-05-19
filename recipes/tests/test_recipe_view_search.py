from unittest.mock import patch

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

    def test_search_recipe_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one', title=title1, author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='two', title=title2, author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

    def test_search_recipe_can_find_recipe_by_description(self):
        description1 = 'this is the description 1'
        description2 = 'this is the description 2'

        recipe1 = self.make_recipe(
            slug='desc-one',
            description=description1,
            author_data={'username': 'descone'}
        )
        recipe2 = self.make_recipe(
            slug='desc-two',
            description=description2,
            author_data={'username': 'desctwo'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={description1}')
        response2 = self.client.get(f'{search_url}?q={description2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])
        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_search_is_paginated(self):
        title = 'Recipe Title'
        for i in range(8):
            kwargs = {'slug': f'r{i}',
                      'author_data': {'username': f'r{i}'},
                      'title': {title}}
            self.make_recipe(**kwargs)

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title}')
        recipes = response1.context['recipes']
        paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(3)), 2)
