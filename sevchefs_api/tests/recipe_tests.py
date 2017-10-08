from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import json

from rest_framework import status
from sevchefs_api.models import Recipe, RecipeTag
from sevchefs_api.tests import base_tests


class AnonymousUserRecipeTests(base_tests.BaseGuestUser):

    def test_guest_user_cannot_comment_recipe(self):
        """
        Ensure guest user cannot comment on recipe
        """
        other_user = User.objects.create_user('other', 'other@api.com', 'testpassword')
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=other_user)

        comment = {'comment': 'my comment'}
        response = self.client.post(reverse('recipe-comment', args=[recipe.id]), json.dumps(comment), 'application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_view_recipe_list(self):
        """
        Ensure guest user can view recipe list
        """
        other_user = User.objects.create_user('other', 'other@api.com', 'testpassword')
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=other_user)

        response = self.client.get(reverse('recipe-list-view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Recipe1')


class RecipeTests(base_tests.BaseApiTest):

    def test_login_user_can_comment_recipe(self):
        """
        Ensure login user can comment on a recipe
        """
        other_user = User.objects.create_user('other', 'other@api.com', 'testpassword')
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=other_user)

        comment = {'comment': 'my comment'}
        response = self.client.post(reverse('recipe-comment', args=[recipe.id]), json.dumps(comment), 'application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_non_exist_recipe_return_404(self):
        """
        Commenting on a recipe that does not exists return 404
        """
        comment = {'comment': 'my comment'}
        response = self.client.post(reverse('recipe-comment', args=[1]), json.dumps(comment), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_recipe_without_comment_body_return_400(self):
        """
        Ensure HTTP_400_BAD_REQUEST return when commenting recipe without any
        comment text
        """
        other_user = User.objects.create_user('other', 'other@api.com', 'testpassword')
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=other_user)

        response = self.client.post(reverse('recipe-comment', args=[recipe.id]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_recipe_details(self):
        """
        Ensure can view details of a recipe
        """
        other_user = User.objects.create_user('other', 'other@api.com', 'testpassword')
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=other_user)

        response = self.client.get(reverse('recipe-view', args=[recipe.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Recipe1')

    def test_login_user_can_create_new_recipe(self):
        """
        Ensure login user can create recipe
        """
        recipe_dict = {'name': 'recipe1', 'description': 'description', 'difficulty': 2}
        response = self.client.post(reverse('recipe-upload'), json.dumps(recipe_dict), 'application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_new_recipe_fail_on_missing_attributes(self):
        """
        Ensure login user can create recipe
        """
        recipe_dict = {'name': 'Recipe1', 'description': '', 'difficulty': 2}
        response = self.client.post(reverse('recipe-upload'), json.dumps(recipe_dict), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        recipe_dict = {'name': '', 'description': 'description', 'difficulty': 2}
        response = self.client.post(reverse('recipe-upload'), json.dumps(recipe_dict), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_tag_to_recipe(self):
        """
        Ensure able to add tag to recipe
        """
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=self.user)
        recipe_tag = RecipeTag.objects.create(text="Meat")
        recipe_tag_list = {'tag_ids': [recipe_tag.id]}

        response = self.client.post(reverse('recipe-add-tag', args=[recipe.id]), json.dumps(recipe_tag_list), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_add_tag_to_recipe_of_other_user(self):
        """
        Ensure other user cannot add tag to a recipe
        """
        other_user = User.objects.create_user('other', 'other@api.com', 'testpassword')
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=other_user)
        recipe_tag = RecipeTag.objects.create(text="Meat")
        recipe_tag_list = {'tag_ids': [recipe_tag.id]}

        response = self.client.post(reverse('recipe-add-tag', args=[recipe.id]), json.dumps(recipe_tag_list), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
