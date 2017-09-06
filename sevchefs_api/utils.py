from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from sevchefs_api.models import *
import json


class RecipeUtils:

    def get_recipe_or_404(id):
        try:
            recipe = Recipe.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise NotFound("Unable to find recipe with id %s" % id)
        return recipe

    def add_recipe_comments(recipe, user, comment):
        RecipeComment.objects.create(recipe=recipe, user=user, text=comment)


def get_request_body_param(request, param):

    body_unicode = request.body.decode('utf-8')

    try:
        body = json.loads(body_unicode)
    except json.decoder.JSONDecodeError:
        return ""

    try:
        body_param_text = body[param]
    except KeyError:
        return ""

    return body_param_text
