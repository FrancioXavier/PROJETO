from django.urls import path

from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', view=views.register_view, name='register'),
    path('register/create/', view=views.register_create, name='register_create'),  # noqa 501
    path('login/', view=views.login_view, name='login'),
    path('login/create/', view=views.login_create, name='login_create'),
    path('logout/', view=views.logout_view, name='logout'),
]
