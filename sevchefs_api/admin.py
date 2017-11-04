from django.contrib import admin
from .models import *


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('name', 'description', 'image')


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = ('name', 'description', 'upload_datetime', 'upload_by_user', 'image', 'difficulty_level')


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ('user', 'description', 'avatar')


class ActivityTimelineAdmin(admin.ModelAdmin):
    model = ActivityTimeline
    list_display = ('user', 'summary_text', 'target_user', 'main_object_image', 'target_object_image', 'datetime')


class RecipeCommentAdmin(admin.ModelAdmin):
    model = RecipeComment
    list_display = ('recipe', 'user', 'text', 'datetime')


class RecipeTagAdmin(admin.ModelAdmin):
    model = RecipeTag
    list_display = ('text',)


class RecipeInstructionAdmin(admin.ModelAdmin):
    model = RecipeInstruction
    list_display = ('recipe', 'step_num', 'instruction', 'time_required', 'image')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ActivityTimeline, ActivityTimelineAdmin)
admin.site.register(RecipeComment, RecipeCommentAdmin)
admin.site.register(RecipeInstruction, RecipeInstructionAdmin)
