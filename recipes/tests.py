from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipes.models import Recipe
from http import HTTPStatus


class RecipesTestPages(TestCase):
    """
    Tests each page's status and template usage.
    """

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="tester", email="tester@email.com", password="pass")
        self.recipe = Recipe.objects.create(
            category="breakfast", name="Toast",
            description="Crispy bread with butter",
            ingredients=("bread", "butter"),
            instructions=("Stick bread in toaster", "Spread butter on bread"),
            submitter=self.user)

    def test_recipe_home_page_status_code(self):
        url = reverse('recipes_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
