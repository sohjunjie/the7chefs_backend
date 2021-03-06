from datetime import timedelta
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import json

from rest_framework import status
from sevchefs_api.models import Recipe, RecipeTag, UserRecipeFavourites, \
    Ingredient, RecipeIngredient, RecipeInstruction, ActivityTimeline
from sevchefs_api.tests import base_tests

from tempfile import mkdtemp
from shutil import rmtree
from django.test.utils import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile


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

    def test_user_can_view_otheruser_recipe_list(self):
        """
        Ensure guest user can view recipe list
        """
        other_user = User.objects.create_user('other', 'other@api.com', 'testpassword')
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=other_user)
        recipe2 = Recipe.objects.create(name='Recipe2', description='Recipe2', upload_by_user=other_user)

        response = self.client.get(reverse('user-recipe-list', args=[other_user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Recipe1')
        self.assertContains(response, 'Recipe2')

    def test_view_nonexist_user_recipe_list_404(self):
        """
        Ensure guest user can view recipe list
        """

        response = self.client.get(reverse('user-recipe-list', args=[123]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_recipe_details(self):
        """
        Ensure can view details of a recipe
        """
        other_user = User.objects.create_user('other', 'other@api.com', 'testpassword')
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=other_user)

        response = self.client.get(reverse('recipe-view', args=[recipe.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Recipe1')

    def test_view_nonexist_recipe_details_404(self):
        """
        Ensure can view details of a recipe
        """
        other_user = User.objects.create_user('other', 'other@api.com', 'testpassword')
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=other_user)

        response = self.client.get(reverse('recipe-view', args=[123]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_guestuser_cannot_favourite_recipe(self):
        """
        Ensure guest user cannot favourite a recipe
        """
        other_user = User.objects.create_user('other', 'other@api.com', 'testpassword')
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=other_user)

        response = self.client.post(reverse('recipe-favourite', args=[recipe.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_guestuser_cannot_unfavourite_recipe(self):
        """
        Ensure guest user cannot favourite a recipe
        """
        other_user = User.objects.create_user('other', 'other@api.com', 'testpassword')
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=other_user)

        response = self.client.delete(reverse('recipe-favourite', args=[recipe.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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
        self.assertEqual(ActivityTimeline.objects.count(), 1)

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

    def test_edit_recipe(self):

        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=self.user)

        data = {'name': 'recipe2', 'description': 'new desc', 'difficulty_level': 3}
        response = self.client.put(reverse('recipe-edit-view', args=[recipe.id]), json.dumps(data), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        newrecipe = Recipe.objects.get(pk=recipe.id)
        self.assertEqual(newrecipe.name, 'recipe2')
        self.assertEqual(newrecipe.description, 'new desc')
        self.assertEqual(newrecipe.difficulty_level, 3)

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

    def test_user_favourite_recipe(self):
        """
        Ensure user can favourite a recipe
        """
        other_user = User.objects.create_user('other', 'other@api.com', 'testpassword')
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=other_user)

        response = self.client.post(reverse('recipe-favourite', args=[recipe.id]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserRecipeFavourites.objects.filter(userprofile=self.user.userprofile).count(), 1)

    def test_user_unfavourite_recipe(self):
        """
        Ensure user can favourite a recipe
        """
        other_user = User.objects.create_user('other', 'other@api.com', 'testpassword')
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=other_user)
        UserRecipeFavourites.objects.create(userprofile=self.user.userprofile, recipe=recipe)

        response = self.client.delete(reverse('recipe-favourite', args=[recipe.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserRecipeFavourites.objects.filter(userprofile=self.user.userprofile).count(), 0)

    def test_add_ingredient_to_recipe(self):
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=self.user)
        ingredient = Ingredient.objects.create(name="onion", description="onion1")

        data = {'serving_size': '100 cubes'}

        response = self.client.post(reverse('recipe-ingredient', args=[recipe.id, ingredient.id]), json.dumps(data), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(recipe.ingredients.count(), 1)

    def test_add_ingredient_to_recipe_by_name(self):
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=self.user)
        ingredient = Ingredient.objects.create(name="onion", description="onion1")

        data = {'serving_size': '100 cubes',
                'ingredient_name': ingredient.name}

        response = self.client.post(reverse('recipe-ingredient-add', args=[recipe.id]), json.dumps(data), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(recipe.ingredients.count(), 1)

    def test_remove_ingredient_from_recipe(self):
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=self.user)
        ingredient = Ingredient.objects.create(name="onion", description="onion1")
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, serving_size="100 cubes")
        response = self.client.delete(reverse('recipe-ingredient', args=[recipe.id, ingredient.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.ingredients.count(), 0)


class RecipeInstructionTest(base_tests.BaseApiTest):

    def test_create_recipe_instruction(self):
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=self.user)

        data = {'recipe_id': recipe.id, 'step_num': 1, 'instruction': "instru1", 'duration_minute': 10, 'duration_hour': 0}
        response = self.client.post(reverse('recipe-instruction-view'), json.dumps(data), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(RecipeInstruction.objects.filter(recipe=recipe).exists())

    def test_create_recipe_instruction_neg_stepnum_invalid(self):
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=self.user)

        data = {'recipe_id': recipe.id, 'step_num': -1, 'instruction': "instru1", 'duration_minute': 10, 'duration_hour': 0}
        response = self.client.post(reverse('recipe-instruction-view'), json.dumps(data), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(RecipeInstruction.objects.filter(recipe=recipe).exists())

    def test_create_recipe_instruction_wo_instruction_invalid(self):
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=self.user)

        data = {'recipe_id': recipe.id, 'step_num': 1, 'instruction': "", 'duration_minute': 10, 'duration_hour': 0}
        response = self.client.post(reverse('recipe-instruction-view'), json.dumps(data), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(RecipeInstruction.objects.filter(recipe=recipe).exists())

    def test_instruction_timerequired_reflected_in_recipe(self):
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=self.user)
        repInstr = RecipeInstruction.objects.create(recipe=recipe, step_num=1, instruction="test", time_required=timedelta(minutes=10))
        repInstr2 = RecipeInstruction.objects.create(recipe=recipe, step_num=2, instruction="test", time_required=timedelta(minutes=5))

        response = self.client.get(reverse('recipe-view', args=[recipe.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, str(timedelta(minutes=15)))

    def test_delete_recipe_instruction_also_decrement_affected_instruction_stepnum(self):
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=self.user)
        repInstr = RecipeInstruction.objects.create(recipe=recipe, step_num=1, instruction="test1", time_required=timedelta(minutes=10))
        repInstr2 = RecipeInstruction.objects.create(recipe=recipe, step_num=2, instruction="test2", time_required=timedelta(minutes=5))

        data = {'recipe_id': recipe.id, 'instruction_id': repInstr.id}
        response = self.client.delete(reverse('recipe-instruction-view'), json.dumps(data), 'application/json')
        updatedRepInstr2 = RecipeInstruction.objects.get(pk=repInstr2.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updatedRepInstr2.step_num, 1)
        self.assertFalse(RecipeInstruction.objects.filter(pk=repInstr.id).exists())


class RecipeImageTest(base_tests.BaseApiTest):

    def setUp(self):
        super(RecipeImageTest, self).setUp()
        self.media_folder = mkdtemp()

    def tearDown(self):
        super(RecipeImageTest, self).tearDown()
        rmtree(self.media_folder)

    def test_cannot_upload_image_to_otheruser_recipe(self):
        with override_settings(MEDIA_ROOT=self.media_folder):
            other_user = User.objects.create_user('other', 'other@api.com', 'testpassword')
            recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=other_user)

            image = SimpleUploadedFile(name='test_image.jpg', content=open('test_image/food.png', 'rb').read(), content_type='image/png')
            form_data = {'image': image}

            response = self.client.post(reverse('recipe-image-upload', args=[recipe.id]), form_data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_upload_recipe_image(self):
        with override_settings(MEDIA_ROOT=self.media_folder):

            recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=self.user)

            image = SimpleUploadedFile(name='test_image.jpg', content=open('test_image/food.png', 'rb').read(), content_type='image/png')
            form_data = {'image': image}
            response = self.client.post(reverse('recipe-image-upload', args=[recipe.id]), form_data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_image(self):
        with override_settings(MEDIA_ROOT=self.media_folder):

            recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=self.user)
            image = SimpleUploadedFile(name='test_image.jpg', content=open('test_image/food.png', 'rb').read(), content_type='image/png')
            form_data = {'image': image}
            response = self.client.post(reverse('recipe-image-upload', args=[recipe.id]), form_data, format='multipart')

            response = self.client.delete(reverse('recipe-image-upload', args=[recipe.id]))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_recipe_instruction_image(self):
        with override_settings(MEDIA_ROOT=self.media_folder):

            recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=self.user)
            recipe_instruction = RecipeInstruction.objects.create(recipe=recipe, step_num=1, instruction="test")

            image = SimpleUploadedFile(name='test_image.jpg', content=open('test_image/food.png', 'rb').read(), content_type='image/png')
            form_data = {'image': image}
            response = self.client.post(reverse('recipe-instruction-image-upload', args=[recipe_instruction.id]), form_data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
