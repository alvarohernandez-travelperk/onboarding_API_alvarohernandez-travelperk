'''
Test for models.
'''
from django.test import TestCase

from core import models


class ModelTests(TestCase):
    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        recipe = models.Recipe.objects.create(
            title='Sample recipe name',
            description='Sample recipe description'
        )

        self.assertEqual(str(recipe), recipe.title)
