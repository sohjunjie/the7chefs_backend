from sevchefs_api.tests import base_tests
from sevchefs_api.utils import *
from sevchefs_api.models import RecipeTag, Ingredient

from rest_framework.exceptions import NotFound


class UtilsTests(base_tests.BaseApiTest):

    def test_get_recipe_tag_or_none_return_none(self):
        non_exist_recipe_tag_id = 1
        recipe_tag = RecipeUtils.get_recipe_tag_or_none(non_exist_recipe_tag_id)
        self.assertIsNone(recipe_tag)

    def test_get_ingredient_or_404_raise_404(self):
        non_exist_ingredient_id = 1
        self.assertRaises(NotFound, RecipeUtils.get_ingredient_or_404,
                          non_exist_ingredient_id)

    def test_get_recipe_instruction_or_404_raise_404(self):
        non_exist_recipe_instruction_id = 1
        self.assertRaises(NotFound, RecipeUtils.get_recipe_instruction_or_404,
                          non_exist_recipe_instruction_id)
