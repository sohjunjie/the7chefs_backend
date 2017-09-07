from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from sevchefs_api.models import UserProfile
from sevchefs_api.utils import get_request_body_param
from sevchefs_api.serializers import UserProfileSerializer


class UserSignUpView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Sign up a user

        @body email: user comment on the recipe
        @body username: user comment on the recipe
        @body password: user comment on the recipe

        @return: http status of query
        @raise HTTP_400_BAD_REQUEST: signup details must not be empty
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


class UserProfileView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, pk):
        """
        View a user profile
        """
        user = User.objects.get(pk=pk)
        user_profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(user_profile)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
