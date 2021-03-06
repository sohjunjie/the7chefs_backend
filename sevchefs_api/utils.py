from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from sevchefs_api.exceptions import NotAuthorized
from sevchefs_api.models import *

import json


class RecipeUtils:

    def get_recipe_or_404(id):
        try:
            recipe = Recipe.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise NotFound("Unable to find recipe with id %s" % id)
        return recipe

    def get_recipe_instruction_or_404(id):
        try:
            recipeInstruction = RecipeInstruction.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise NotFound("Unable to find recipe instruction with id %s" % id)
        return recipeInstruction

    def get_ingredient_or_404(id):
        try:
            ingredient = Ingredient.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise NotFound("Unable to find ingredient with id %s" % id)
        return ingredient

    def add_recipe_comments(recipe, user, comment):
        RecipeComment.objects.create(recipe=recipe, user=user, text=comment)

    def get_recipe_tag_or_none(id):
        try:
            tag = RecipeTag.objects.get(pk=id)
        except ObjectDoesNotExist:
            tag = None
        return tag

    def delete_recipe_image(recipe):
        recipe.image.delete()
        return True

    def delete_recipe_instruction_image(recipe_instruction):
        recipe_instruction.image.delete()
        return True

    def raise_401_if_recipe_not_belong_user(recipe, request):
        if recipe.upload_by_user != request.user:
            raise NotAuthorized('only creator of recipe can edit')


class UserUtils:

    def get_user_or_404(id):
        try:
            user = User.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise NotFound("Unable to find user with id %s" % id)
        return user


def get_request_body_param(request, param, return_on_error):

    body_unicode = request.body.decode('utf-8')
    try:
        body = json.loads(body_unicode)
    except json.decoder.JSONDecodeError:
        return return_on_error

    try:
        body_param_text = body[param]
    except KeyError:
        return return_on_error

    return body_param_text
