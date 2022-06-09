from authors.forms import AuthorRecipeForm
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from recipes.models import Recipe


class DashboardRecipe(View):
    def get_recipe(self, id):
        try:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

        except Recipe.DoesNotExist:
            raise Http404()

        return recipe

    def form(self, id):
        recipes = self.get_recipe(id)

        form = AuthorRecipeForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
            instance=recipes,
        )
        return form

    def render(self, request, form):
        return render(request, 'authors/pages/edit_recipe.html', context={
            'form': form,
        })

    def get(self, request, id):
        form = self.form(id)

        return self.render(request, form)

    def post(self, request, id):
        form = self.form(id)

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()
            messages.success(request, 'Sua receita foi salva com sucesso.')

            return redirect(reverse('authors:edit_recipe', args=(id,)))

        return self.render(request, form)
