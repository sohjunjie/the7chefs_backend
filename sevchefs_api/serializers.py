from django.contrib.auth.models import User
from rest_framework import serializers
from sevchefs_api.models import *

from datetime import timedelta


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class IngredientSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'description', 'image_url')

    def get_image_url(self, ingredient):

        if not ingredient.image:
            return None

        image_url = ingredient.image.url
        return image_url


class RecipeIngredientSerializer(serializers.ModelSerializer):

    ingredient = IngredientSerializer(many=False)

    class Meta:
        model = RecipeIngredient
        fields = ('recipe', 'ingredient', 'serving_size')


class RecipeSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(many=True)
    is_favourited = serializers.SerializerMethodField()
    time_required = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'upload_by_user', 'difficulty_level',
                  'time_required', 'upload_datetime', 'image_url', 'ingredients',
                  'is_favourited')

    def get_time_required(self, recipe):
        return_time_required = timedelta(0)
        for instr in recipe.instructions.all():
            return_time_required += instr.time_required
        return str(return_time_required)

    def get_image_url(self, recipe):

        if not recipe.image:
            return None

        image_url = recipe.image.url
        return image_url

    def get_is_favourited(self, recipe):

        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        if user is None or user.is_anonymous():
            return False

        if not user.userprofile.favourited_recipes.filter(id=recipe.id).exists():
            return False

        return True


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


class RecipeInstructionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeInstruction
        fields = ('image', )
