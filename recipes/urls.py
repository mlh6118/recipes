from django.urls import path
from .views import HomePageView, RecipeDetailView, RecipeCreateView, \
    RecipeUpdateView, RecipeDeleteView

urlpatterns = [
    path("", HomePageView.as_view(), name="recipes_home"),
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('update/<int:pk>', RecipeUpdateView.as_view(), name='recipe_update'),
    path('delete/<int:pk>', RecipeDeleteView.as_view(), name='recipe_delete'),
]