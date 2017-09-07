from sevchefs_api.tests import base_tests
from sevchefs_api.utils import *
from sevchefs_api.models import RecipeTag


class UtilsTests(base_tests.BaseApiTest):

    def test_get_recipe_tag_or_none_return_none(self):
        non_exist_recipe_tag_id = 1
        recipe_tag = RecipeUtils.get_recipe_tag_or_none(1)
        self.assertIsNone(recipe_tag)
