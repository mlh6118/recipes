from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


CATEGORY_CHOICES = (
    ('', ''),
    ('breakfast', 'BREAKFAST'),
    ('hors_devours', 'HORS D\'OEUVRES'),
    ('soup', 'SOUP'),
    ('salad', 'SALAD'),
    ('beef', 'BEEF'),
    ('fish', 'FISH'),
    ('poultry', 'POULTRY')
)


class Recipe(models.Model):
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES,
                                default='')
    name = models.CharField(max_length=128)
    description = models.TextField(default="")
    ingredients = models.TextField(default="")
    instructions = models.TextField(default="")
    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipe_detail', args=[str(self.id)])
