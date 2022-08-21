from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView
from .models import Recipe
from django.urls import reverse_lazy


class HomePageView(ListView):
    template_name = "pages/recipes_home.html"
    model = Recipe
    context_object_name = 'recipes_list'


class RecipeDetailView(DetailView):
    template_name = 'pages/recipe_detail.html'
    model = Recipe


class RecipeCreateView(CreateView):
    template_name = 'pages/recipe_create.html'
    model = Recipe
    fields = ['category', 'name', 'description', 'ingredients',
              'instructions', 'submitter']


class RecipeUpdateView(UpdateView):
    template_name = 'pages/recipe_update.html'
    model = Recipe
    fields = ['category', 'name', 'description', 'ingredients',
              'instructions', 'submitter']


class RecipeDeleteView(DeleteView):
    template_name = 'pages/recipe_delete.html'
    model = Recipe
    success_url = reverse_lazy('recipes_home')