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
            category="breakfast",
            name="Toast",
            description="Crispy bread with butter",
            ingredients="bread \n butter",
            instructions="Stick bread in toaster \n Spread butter on bread",
            submitter=self.user)

    def test_recipe_home_page_status_code(self):
        url = reverse('recipes_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_page_template(self):
        url = reverse("recipes_home")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "pages/recipes_home.html")
        self.assertTemplateUsed(response, "_base.html")

    def test_recipe_detail_page_status_code(self):
        url = reverse('recipe_detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_page_template(self):
        url = reverse("recipe_detail", args=[1])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "pages/recipe_detail.html")
        self.assertTemplateUsed(response, "_base.html")

    def test_recipe_create_page_status_code(self):
        url = reverse('recipe_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_create_page_template(self):
        url = reverse("recipe_create")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "pages/recipe_create.html")
        self.assertTemplateUsed(response, "_base.html")

    def test_recipe_update_page_status_code(self):
        url = reverse('recipe_update', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_update_page_template(self):
        url = reverse("recipe_update", args=[1])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "pages/recipe_update.html")
        self.assertTemplateUsed(response, "_base.html")

    def test_recipe_delete_page_status_code(self):
        url = reverse('recipe_delete', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_delete_page_template(self):
        url = reverse("recipe_delete", args=[1])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "pages/recipe_delete.html")
        self.assertTemplateUsed(response, "_base.html")

    """
    Test each element of a recipe on each page.
    """

    def test_string_representation(self):
        self.assertEqual(str(self.recipe), 'Toast')

    def test_string_representation_fail(self):
        self.assertIsNot(str(self.recipe), 'toast')

    def test_string_representation_name(self):
        self.assertEqual(str(self.recipe.name), 'Toast')

    def test_string_representation_title_fail(self):
        self.assertIsNot(str(self.recipe.name), 'Reeses')

    def test_string_representation_description(self):
        self.assertEqual(str(self.recipe.description), 'Crispy bread with '
                                                       'butter')

    def test_string_representation_description_fail(self):
        self.assertIsNot(str(self.recipe.description), 'Yummy!')

    def test_string_representation_submitter(self):
        self.assertEqual(str(self.recipe.submitter), 'tester')

    def test_string_representation_submitter_fail(self):
        self.assertIsNot(str(self.recipe.submitter), 'admin')


class IntegrationTests(TestCase):
    """
    Test the forms on all pages for posting.
    Code guided by Joey Marianer.
    """

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="tester", email="tester@email.com", password="pass")

    def test_form_create(self):
        response = self.client.post(
            "/recipes/create/",
            data={"category": "breakfast",
                  "name": "Toast",
                  "description": "Crispy bread with butter",
                  "ingredients": "bread \n butter",
                  "instructions": "Stick bread in toaster \n "
                                  "Spread butter on bread",
                  "submitter": self.user.id})

        Rog = Recipe.objects.get(id=1)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue("Location" in response.headers)
        self.assertEqual(response.headers["Location"], "/recipes/1/")
        self.assertEqual(Rog.category, "breakfast")
        self.assertEqual(Rog.name, "Toast")
        self.assertEqual(Rog.description,
                         "Crispy bread with butter")
        self.assertEqual(Rog.ingredients, "bread \n butter")
        self.assertEqual(Rog.instructions, "Stick bread in toaster \n Spread "
                                           "butter on bread")
        self.assertEqual(Rog.submitter.username, "tester")

    def test_form_update(self):
        recipe = Recipe.objects.create(
            category="breakfast",
            name="Toast",
            description="Crispy bread with butter",
            ingredients="bread \n butter",
            instructions="Stick bread in toaster \n Spread butter on bread",
            submitter=self.user)

        response = self.client.post(
            f"/recipes/update/{recipe.id}",
            data={"category": "soup",
                  "name": "Split Pea Soup",
                  "description": "soup made of split peas and ham",
                  "ingredients": "peas \n ham \n water",
                  "instructions": "Cook peas and add ham",
                  "submitter": self.user.id})

        # Ensures data in the object called recipe in memory is refreshed from
        # the database to correct data instead of using the
        # Recipe.objects.create(...) from above.
        recipe.refresh_from_db()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue("Location" in response.headers)
        self.assertEqual(response.headers["Location"], f"/recipes/{recipe.id}/")
        self.assertEqual(recipe.category, "soup")
        self.assertEqual(recipe.name, "Split Pea Soup")
        self.assertEqual(recipe.description,
                         "soup made of split peas and ham")
        self.assertEqual(recipe.ingredients, "peas \n ham \n water")
        self.assertEqual(recipe.instructions, "Cook peas and add ham")
        self.assertEqual(recipe.submitter.username, "tester")

    def test_delete_recipe(self):
        recipe = Recipe.objects.create(
            category="breakfast",
            name="Toast",
            description="Crispy bread with butter",
            ingredients="bread \n butter",
            instructions="Stick bread in toaster \n Spread butter on bread",
            submitter=self.user)

        # Check if there is one recipe in the database.
        self.assertEqual(Recipe.objects.count(), 1)

        response = self.client.post(f"/recipes/delete/{recipe.id}",)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # Check if there are no recipes in the database.
        self.assertEqual(Recipe.objects.count(), 0)
