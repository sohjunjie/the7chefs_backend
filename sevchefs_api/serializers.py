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

    upload_by_user = UserSerializer(many=False)
    image_url = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'upload_by_user', 'difficulty_level',
                  'time_required', 'upload_datetime', 'image_url', 'ingredients')

    def get_image_url(self, recipe):

        request = self.context.get('request')
        if not (recipe.image and request):
            return None

        image_url = recipe.image.url
        request = self.context.get('request')
        return request.build_absolute_uri(image_url)


class UserProfileSerializer(serializers.ModelSerializer):

    avatar_url = serializers.SerializerMethodField()
    user = UserSerializer(many=False)

    class Meta:
        model = UserProfile
        fields = ('user', 'description', 'avatar_url')

    def get_avatar_url(self, user_profile):

        request = self.context.get('request')
        if not (user_profile.avatar and request):
            return None

        avatar_url = user_profile.avatar.url
        request = self.context.get('request')
        return request.build_absolute_uri(avatar_url)


class RecipeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('image', )
