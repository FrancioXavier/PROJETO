from django.urls import path

from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/search/',
         views.RecipeListViewSearch.as_view(), name='search'),
    path('recipes/category/<int:category_id>/',
         views.RecipeListViewCategory.as_view(), name="category"),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe'),
    path('recipes/api/v1/',
         views.RecipeListViewHomeApi.as_view(), name='home_api'),
    path('recipes/api/v1/<int:pk>',
         views.RecipeDetailViewApi.as_view(), name='detail_recipe_api'),
]
