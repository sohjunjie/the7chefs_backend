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
