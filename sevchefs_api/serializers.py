from django.contrib.auth.models import User
from rest_framework import serializers
from sevchefs_api.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'description')


class RecipeIngredientSerializer(serializers.ModelSerializer):

    ingredient = IngredientSerializer(many=False)

    class Meta:
        model = RecipeIngredient
        fields = ('recipe', 'ingredient', 'serving_size')


# TODO: return image url
# TODO: include recipe ingredient in serializer
class RecipeSerializer(serializers.ModelSerializer):

    upload_by_user = UserSerializer(many=False)
    image_url = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'upload_by_user', 'difficulty_level',
                  'time_required', 'upload_datetime', 'image_url', 'ingredients')

    def get_image_url(self, recipe):

        if not recipe.image:
            return ""

        image_url = recipe.image.url
        request = self.context.get('request')
        return request.build_absolute_uri(image_url)
