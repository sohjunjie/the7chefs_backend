from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import json

from rest_framework import status
from rest_framework.authtoken.models import Token

from sevchefs_api.tests import base_tests
from sevchefs_api.models import ActivityTimeline, Recipe

from tempfile import mkdtemp
from shutil import rmtree
from django.test.utils import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile


class UserTests(base_tests.BaseGuestUser):
    def test_guest_auth_token_w_email_and_password(self):
        """
        Ensure able to get auth token by email and password
        """
        superuser = User.objects.create_superuser('test', 'test@api.com', 'testpassword')
        token = Token.objects.get(user=superuser)

        logindata = {'email': 'test@api.com',
                     'password': 'testpassword'}

        response = self.client.post(reverse('auth-token-view'), json.dumps(logindata), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, token.key)

    def test_guest_auth_token_does_not_exist(self):
        """
        Ensure able to get auth token by email and password
        """

        logindata = {'email': 'test@api.com',
                     'password': 'testpassword'}

        response = self.client.post(reverse('auth-token-view'), json.dumps(logindata), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_guest_auth_token_send_wo_username_password(self):
        """
        Ensure able to get auth token by email and password
        """

        logindata = {'email': '', 'password': ''}
        response = self.client.post(reverse('auth-token-view'), json.dumps(logindata), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_guest_user_sign_up_ok(self):
        """
        Ensure guest user can sign up
        """
        signup_details = {'username': 'user1',
                          'email': 'user1@example.com',
                          'password': 'password1'}

        response = self.client.post(reverse('user-signup'), json.dumps(signup_details), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_guest_user_sign_up_400_when_username_taken(self):
        """
        Ensure guest user can sign up
        """
        userOne = User.objects.create(username="user1", password="qwe123qwe123")
        signup_details = {'username': 'user1',
                          'email': 'user2@example.com',
                          'password': 'password2'}

        response = self.client.post(reverse('user-signup'), json.dumps(signup_details), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_w_missing_details_return_400(self):
        """
        Ensure signup is rejected if missing fields provided
        """
        signup_details = {'username': '', 'email': 'user1@example.com', 'password': 'password1'}
        response = self.client.post(reverse('user-signup'), json.dumps(signup_details), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        signup_details = {'username': 'user1', 'email': '', 'password': 'password1'}
        response = self.client.post(reverse('user-signup'), json.dumps(signup_details), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        signup_details = {'username': 'user1', 'email': 'user1@example.com', 'password': ''}
        response = self.client.post(reverse('user-signup'), json.dumps(signup_details), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_profile(self):
        """
        Ensure able to view user profile
        """
        user = User.objects.create_user('test', 'test@api.com', 'testpassword')
        response = self.client.get(reverse('user-profile-detail', args=[user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_user_profile(self):
        """
        Ensure able to view all user profile
        """
        user = User.objects.create_user('test', 'test@api.com', 'testpassword')
        response = self.client.get(reverse('user-all-detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FollowUnfollowApiTest(base_tests.BaseApiTest):
    def test_follow_user_success(self):
        """
        ensure user can successfully follow someone
        """
        userOne = User.objects.create(username='user1', password='qwe123qwe123')
        userTwo = User.objects.create(username='user2', password='qwe123qwe123')

        response = self.client.post(reverse('user-follow', args=[userOne.userprofile.user_id]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('user-follow', args=[userTwo.userprofile.user_id]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.user.userprofile.follows.filter(pk=userOne.userprofile.user_id).exists())
        self.assertTrue(self.user.userprofile.follows.filter(pk=userTwo.userprofile.user_id).exists())
        self.assertEqual(ActivityTimeline.objects.count(), 2)

    def test_unfollow_user_success(self):
        """
        ensure user can successfully unfollow someone
        """
        userOne = User.objects.create(username='user1', password='qwe123qwe123')
        userTwo = User.objects.create(username='user2', password='qwe123qwe123')

        self.user.userprofile.follows.add(userOne.userprofile)
        self.user.userprofile.follows.add(userTwo.userprofile)

        response = self.client.delete(reverse('user-follow', args=[userOne.userprofile.user_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse('user-follow', args=[userTwo.userprofile.user_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user.userprofile.follows.filter(pk=userOne.userprofile.user_id).exists())
        self.assertFalse(self.user.userprofile.follows.filter(pk=userTwo.userprofile.user_id).exists())

    def test_follow_nonexist_user(self):
        """
        Ensure correct HTTP Response generated when following non-existing user
        """
        response = self.client.post(reverse('user-follow', args=[123]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_already_follow_user(self):
        """
        Ensure correct HTTP Response generated when user already followed
        """
        userOne = User.objects.create(username='user1', password='qwe123qwe123')
        self.user.userprofile.follows.add(userOne.userprofile)

        response = self.client.post(reverse('user-follow', args=[userOne.userprofile.user_id]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_nonexists_user(self):
        """
        Ensure correct HTTP Response generated when unfollowing non-existing user
        """
        response = self.client.delete(reverse('user-follow', args=[123]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_already_unfollow_user(self):
        """
        Ensure correct HTTP Response generated when unfollowing already unfollowed user
        """
        userOne = User.objects.create(username='user1', password='qwe123qwe123')

        response = self.client.delete(reverse('user-follow', args=[userOne.userprofile.user_id]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ActivityTimelineApiTest(base_tests.BaseApiTest):

    def setUp(self):
        super(ActivityTimelineApiTest, self).setUp()
        self.media_folder = mkdtemp()

    def tearDown(self):
        super(ActivityTimelineApiTest, self).tearDown()
        rmtree(self.media_folder)

    def test_recipe_upload_timeline_created(self):
        with override_settings(MEDIA_ROOT=self.media_folder):
            recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=self.user)

            image = SimpleUploadedFile(name='test_image.jpg', content=open('test_image/food.png', 'rb').read(), content_type='image/png')
            form_data = {'image': image}
            response = self.client.post(reverse('recipe-image-upload', args=[recipe.id]), form_data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(ActivityTimeline.objects.count(), 1)
            timeline = ActivityTimeline.objects.first()
            self.assertEqual(timeline.get_formatted_summary_text(self.user), "you uploaded a new recipe")

    def test_favourite_recipe_timeline_created(self):
        other_user = User.objects.create_user('other', 'other@api.com', 'testpassword')
        recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=other_user)

        response = self.client.post(reverse('recipe-favourite', args=[recipe.id]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ActivityTimeline.objects.count(), 1)
        timeline = ActivityTimeline.objects.first()
        self.assertEqual(timeline.get_formatted_summary_text(self.user), "you favourited " + other_user.username + "'s recipe")

    def test_follow_user_timeline_created(self):
        userOne = User.objects.create(username='user1', password='qwe123qwe123')
        response = self.client.post(reverse('user-follow', args=[userOne.userprofile.user_id]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ActivityTimeline.objects.count(), 1)
        timeline = ActivityTimeline.objects.first()
        self.assertEqual(timeline.get_formatted_summary_text(self.user), "you followed " + userOne.username + " on CookTasty")

    def test_activity_timeline_list_view(self):
        with override_settings(MEDIA_ROOT=self.media_folder):
            # upload recipe simulate
            recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=self.user)
            image = SimpleUploadedFile(name='test_image.jpg', content=open('test_image/food.png', 'rb').read(), content_type='image/png')
            form_data = {'image': image}
            responseOne = self.client.post(reverse('recipe-image-upload', args=[recipe.id]), form_data, format='multipart')

            # follow user simulate
            userOne = User.objects.create(username='user1', email='user1@api.com', password='qwe123qwe123')
            responseTwo = self.client.post(reverse('user-follow', args=[userOne.userprofile.user_id]))

            # favourite recipe simulate
            userTwo = User.objects.create_user(username='user2', email='user2@api.com', password='testpassword')
            recipe = Recipe.objects.create(name='Recipe1', description='Recipe1', upload_by_user=userTwo)
            responseThree = self.client.post(reverse('recipe-favourite', args=[recipe.id]))

            testResponse = self.client.get(reverse('user-activity-timeline'))
            self.assertEqual(testResponse.status_code, status.HTTP_200_OK)
            self.assertEqual(ActivityTimeline.objects.count(), 3)
