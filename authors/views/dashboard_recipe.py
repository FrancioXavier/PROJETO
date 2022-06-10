from authors.forms import AuthorRecipeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from recipes.models import Recipe


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipe(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, *args, **kwargs):
        return super().setup(*args, **kwargs)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_recipe(self, id=None):
        recipe = None

        if id is not None:
            try:
                recipe = Recipe.objects.filter(
                    is_published=False,
                    author=self.request.user,
                    pk=id,
                ).first()

            except Recipe.DoesNotExist:
                raise Http404()
        return recipe

    def form(self, id=None):
        if id:
            recipes = self.get_recipe(id)

            form = AuthorRecipeForm(
                data=self.request.POST or None,
                files=self.request.FILES or None,
                instance=recipes,
            )
            return form
        else:
            form = AuthorRecipeForm(
                data=self.request.POST or None,
                files=self.request.FILES or None,
            )
            return form

    def render(self, request, form):
        return render(request, 'authors/pages/edit_recipe.html', context={
            'form': form,
        })

    def get(self, request, id=None):
        form = self.form(id)

        return self.render(request, form)

    def post(self, request, id=None):
        form = self.form(id)

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()
            messages.success(request, 'Sua receita foi salva com sucesso.')

            return redirect(reverse(
                'authors:edit_recipe', args=(
                    recipe.id,
                )
            ))

        return self.render(request, form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))

        recipe.delete()
        messages.success(self.request, 'Deleted successfully.')
        return redirect(reverse('authors:dashboard'))
