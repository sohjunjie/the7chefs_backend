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


class RecipeSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'upload_by_user', 'difficulty_level',
                  'time_required', 'upload_datetime', 'image_url', 'ingredients')

    def get_image_url(self, recipe):

        if not recipe.image:
            return None

        image_url = recipe.image.url
        return image_url


class UserProfileSerializer(serializers.ModelSerializer):

    avatar_url = serializers.SerializerMethodField()
    user = UserSerializer(many=False)

    class Meta:
        model = UserProfile
        fields = ('user', 'description', 'avatar_url')

    def get_avatar_url(self, user_profile):

        if not user_profile.avatar:
            return None

        avatar_url = user_profile.avatar.url
        return avatar_url


class RecipeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('image', )
