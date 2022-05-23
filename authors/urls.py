from django.urls import path

from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', view=views.register_view, name='register'),
    path('register/create/', view=views.register_create, name='create')
]
