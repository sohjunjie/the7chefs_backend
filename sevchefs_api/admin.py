from django.contrib import admin
from .models import *


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('name', 'description', 'image')


admin.site.register(Ingredient, IngredientAdmin)
