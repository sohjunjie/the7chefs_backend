from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from sevchefs_api.utils import get_request_body_param


class UserSignUpView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Sign up a user

        @body email: user comment on the recipe
        @body username: user comment on the recipe
        @body password: user comment on the recipe

        @return: http status of query
        @raise HTTP_401_UNAUTHORIZED: user must be login
        @raise HTTP_404_NOT_FOUND: must be a valid recipe id
        @raise HTTP_400_BAD_REQUEST: recipe comment must not be empty
        """

        email = get_request_body_param(request, 'email')
        password = get_request_body_param(request, 'password')
        username = get_request_body_param(request, 'username')

        if email == "":
            return Response({'detail': 'email must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        if username == "":
            return Response({'detail': 'username must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        if password == "":
            return Response({'detail': 'password must not be empty'}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username, email, password)
        return Response({'data': 'success'}, status=status.HTTP_201_CREATED)
