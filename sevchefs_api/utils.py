from rest_framework.exceptions import NotFound
from sevchefs_api.models import *


class RecipeUtils:

    def get_recipe_or_404(id):
        try:
            recipe = Recipe.objects.get(pk=id)
        except Recipe.DoesNotExist():
            raise NotFound("Unable to find recipe with id %s" % id)
        return recipe
