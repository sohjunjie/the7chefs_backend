import uuid
from django.db import models
from django.contrib.auth.models import User


def user_avatar_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'user/{0}/{1}'.format(instance.id, filename)


def recipe_image_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'recipe/{0}/{1}'.format(instance.id, filename)


def ingredient_image_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'ingredient/{0}'.format(filename)


def recipe_instruction_image_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'recipe/{0}/{1}/{2}/'.format(instance.recipe.id, instance.id, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="userprofile")
    description = models.TextField(max_length=500, null=True)
    avatar = models.ImageField(upload_to=user_avatar_directory_path, blank=True, null=True)
    follows = models.ManyToManyField('UserProfile', related_name='followed_by', blank=True)
    favourited_recipes = models.ManyToManyField(
        'Recipe',
        through='UserRecipeFavourites',
        through_fields=('userprofile', 'recipe'),
    )

    def __str__(self):
        return self.user.username

    def following_count(self):
        return self.follows.all().count()

    def followers_count(self):
        return self.followed_by.all().count()


class ActivityTimeline(models.Model):
    user = models.ForeignKey(User, related_name="timeline")
    summary_text = models.TextField(max_length=200, null=False, blank=False)
    target_user = models.ForeignKey(User, related_name="mentioned_timeline", null=True)
    main_object_image = models.ImageField(blank=True, null=True)
    target_object_image = models.ImageField(blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def get_formatted_summary_text(self, user):
        # summary text is about following
        aboutfollow = True if "follow" in self.summary_text else False
        if self.target_user is None:
            if self.user.id == user.id:
                return self.summary_text.format("you")
            return self.summary_text.format(self.target_user.username)

        # you followed yourself, you favourited your recipe, you commented on your recipe
        if (user.id == self.user.id) and (user.id == self.target_user.id):
            if aboutfollow:
                return self.summary_text.format("you", "yourself")
            return self.summary_text.format("you", "your")

        # you followed someone, you favourited someone recipe, you commented on someone recipe
        elif user.id == self.user.id:
            if aboutfollow:
                return self.summary_text.format("you", self.target_user.username)
            return self.summary_text.format("you", self.target_user.username + "'s")

        # someone followed you, someone favourited your recipe, someone commented on your recipe
        elif self.target_user.id == user.id:
            if aboutfollow:
                return self.summary_text.format(self.target_user.username, "you")
            return self.summary_text.format(self.target_user.username, "your")

        return self.summary_text.format(self.user.username, self.target_user.username)


class Recipe(models.Model):
    name = models.TextField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    upload_datetime = models.DateTimeField(auto_now_add=True)
    upload_by_user = models.ForeignKey(User, related_name='recipes')
    image = models.ImageField(upload_to=recipe_image_directory_path, blank=True, null=True)
    difficulty_level = models.IntegerField(default=0)
    ingredients_list = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
    )
    favourited_by = models.ManyToManyField(
        UserProfile,
        through='UserRecipeFavourites',
        through_fields=('recipe', 'userprofile'),
    )
    tags = models.ManyToManyField(
        'RecipeTag',
        through='RecipeTagTable',
        through_fields=('recipe', 'tag'),
    )

    def __str__(self):
        return self.name

    def get_recipe_tags(self):
        return self.tags.all()

    def get_recipe_ingredients(self):
        return self.ingredients.all()

    def get_favourited_count(self):
        return self.favourited_by.all().count()

    def get_image_url(self):
        return str(self.image)


class RecipeComment(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='comments')
    user = models.ForeignKey(User, related_name='recipe_comments')
    text = models.TextField(max_length=500, null=False, blank=False)
    datetime = models.DateTimeField(auto_now_add=True)


class UserRecipeFavourites(models.Model):
    userprofile = models.ForeignKey(UserProfile)
    recipe = models.ForeignKey(Recipe)
    datetime = models.DateTimeField(auto_now_add=True)


class RecipeInstruction(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='instructions')
    step_num = models.IntegerField(default=1)
    instruction = models.TextField(max_length=140, null=False, blank=False)
    time_required = models.DurationField(null=True)
    image = models.ImageField(upload_to=recipe_instruction_image_directory_path, blank=True, null=True)

    class Meta:
        ordering = ['step_num']


class Ingredient(models.Model):
    name = models.TextField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to=ingredient_image_directory_path, null=True, blank=True)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="ingredients")
    ingredient = models.ForeignKey(Ingredient)
    serving_size = models.TextField()


class RecipeTag(models.Model):
    text = models.TextField(blank=False, null=False, unique=True)


class RecipeTagTable(models.Model):
    recipe = models.ForeignKey(Recipe)
    tag = models.ForeignKey(RecipeTag)
