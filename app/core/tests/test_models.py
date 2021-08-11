from django.test import TestCase

from core import models


class ModelTests(TestCase):

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            name='Catalan sausage with white beans',
            description='The simplest and bestest catalan recipe!',
        )
        self.assertEqual(str(recipe), recipe.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            name='Beans',
        )
        self.assertEqual(str(ingredient), ingredient.name)