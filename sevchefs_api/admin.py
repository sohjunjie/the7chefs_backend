from django.contrib import admin
from .models import *


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('name', 'description', 'image')


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = ('name', 'description', 'upload_datetime', 'upload_by_user', 'image', 'difficulty_level')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
