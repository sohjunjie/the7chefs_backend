from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import json

from rest_framework import status
from sevchefs_api.tests import base_tests


class UserTests(base_tests.BaseGuestUser):
    def test_guest_user_sign_up_ok(self):
        """
        Ensure guest user can sign up
        """
        signup_details = {'username': 'user1',
                          'email': 'user1@example.com',
                          'password': 'password1'}

        response = self.client.post(reverse('user-signup'), json.dumps(signup_details), 'application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
