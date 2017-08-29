from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.TextField(max_length=500, null=True)
    avatar = models.ImageField(blank=True, null=True)
    favourited_recipes = models.ManyToManyField(
        'Recipe',
        through='UserRecipeFavourites',
        through_fields=('userprofile', 'recipe'),
    )

    def __str__(self):
        return self.user.username


class Recipe(models.Model):
    name = models.TextField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    upload_datetime = models.DateTimeField(auto_now_add=True)
    upload_by_user = models.ForeignKey(User, related_name='Recipes')
    image = models.ImageField(blank=True, null=True)
    difficulty_level = models.IntegerField(default=0)
    time_required = models.DurationField()
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
    )
    favourited_by = models.ManyToManyField(
        UserProfile,
        through='UserRecipeFavourites',
        through_fields=('recipe', 'userprofile'),
    )

    def favourited_count(self):
        return self.favourited_by.all().count()


class UserRecipeFavourites(models.Model):
    userprofile = models.ForeignKey(UserProfile)
    recipe = models.ForeignKey(Recipe)
    datetime = models.DateTimeField(auto_now_add=True)


class RecipeInstruction(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='Recipe')
    step_num = models.IntegerField(default=1)
    instruction = models.TextField(max_length=500, null=False, blank=False)
    image = models.ImageField(blank=True, null=True)


class Ingredient(models.Model):
    name = models.TextField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=200)
    image = models.ImageField(null=True, blank=True)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    serving_size = models.TextField()
