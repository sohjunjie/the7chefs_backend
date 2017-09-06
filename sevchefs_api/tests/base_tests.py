from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase


class BaseApiTest(TestCase):
    def setUp(self):
        superuser = User.objects.create_superuser('test', 'test@api.com', 'testpassword')
        self.user = superuser
        self.client.login(username=superuser.username, password='testpassword')


class BaseLoginUser(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', 'test@api.com', 'testpassword')
        self.factory = RequestFactory()
        self.user = user
        self.client.login(username=user.username, password='testpassword')


class BaseGuestUser(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnonymousUser()
