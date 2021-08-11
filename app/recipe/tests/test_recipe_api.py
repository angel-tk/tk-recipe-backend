from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Return Recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])

def sample_recipe(**params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'Sample recipe name',
        'description': 'Sample recipe description.'
    }
    defaults.update(params)
    return Recipe.objects.create(**defaults)


class RecipeApiTests(TestCase):
    """Test unauthenticated recipe API access"""
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        """Test retrieving list of the recipes"""
        sample_recipe(name='Recipe one')
        sample_recipe(name='Recipe two')

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe_succesful(self):
        """Test creating recipe"""
        payload = {
            'name': 'Mac and cheese',
            'description': 'Cook macaroni, add loads of cheddad, put it in the oven.',
            "ingredients": [
                {"name": "macaroni"}, {"name": "cheddad"}]
        }

        res = self.client.post(RECIPES_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        serializer = RecipeSerializer(recipe)
        self.assertEqual(serializer.data, res.data)

    def test_create_recipe_unsuccesful(self):
        """Test creating a recipe unsucessful"""
        payload = {
            'name': '',
            'description': '',
        }
        res = self.client.post(RECIPES_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_without_ingredients(self):
        """Test creating a recipe without ingredients"""
        payload = {
            'name': 'Nutella crepe',
            'description': 'The sweetest meal.',
            'ingredients': []
        }
        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 0)

    def test_patch_recipe(self):
        """Test partially updating the recipe"""
        recipe = sample_recipe()
        payload = {'name': 'Cuban rice', 'ingredients': [{'name': 'rice'}, {'name': 'eggs'}]}

        url = detail_url(recipe.id)
        self.client.patch(url, payload, format='json')

        recipe.refresh_from_db()
        self.assertEqual(recipe.name, payload['name'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(len(ingredients), 2)

    def test_full_update_recipe(self):
        """Test updating the whole recipe with put"""
        recipe = sample_recipe()
        payload = {
            'name': 'Irish beef stew',
            'description': 'Food for your soul.',
            'ingredients': [{'name': 'mutton'}]
        }

        url = detail_url(recipe.id)
        self.client.put(url, payload, format="json")

        recipe.refresh_from_db()
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(len(ingredients), 1)

    def test_filter_recipes_by_name_starts_with(self):
        """Test retrieving a list of recipes filtering by name substring"""
        recipe1 = sample_recipe(name='Paella')
        recipe2 = sample_recipe(name='Pizza Tarradellas')
        recipe3 = sample_recipe(name='Irish breakfast')

        res = self.client.get(RECIPES_URL,{'name': 'piz'})

        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        serializer3 = RecipeSerializer(recipe3)

        self.assertEqual(len(res.data), 1)
        self.assertNotIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_delete_recipe(self):
        """ Test that recipe deletes succesfully"""
        recipe = sample_recipe()
        url = detail_url(recipe.id)
        res = self.client.delete(url)
        
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)