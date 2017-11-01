from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import Http404

from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from sevchefs_api.models import UserProfile
from sevchefs_api.utils import get_request_body_param
from sevchefs_api.serializers import UserProfileSerializer

import re


class ObtainAuthToken(APIView):

    permission_classes = (AllowAny, )

    def post(self, request):

        username = get_request_body_param(request, 'email', '')
        password = get_request_body_param(request, 'password', '')

        if not (username and password):
            return Response({"detail": "credentials not entered"}, status.HTTP_400_BAD_REQUEST)

        email_regex_pattern = '^([\w\.]+)@((?:[\w]+\.)+)([a-zA-Z]{2,4})$'
        if re.search(email_regex_pattern, username) is not None:
            try:
                username = User.objects.get(email=username).username
            except User.DoesNotExist:
                username = None

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"non_field_errors": ["Unable to log in with provided credentials."]}, status.HTTP_400_BAD_REQUEST)

        token = Token.objects.get(user=user)
        return Response({"token": token.key}, status.HTTP_200_OK)


class UserSignUpView(APIView):

    permission_classes = (AllowAny,)

    def response_with_400(self, info):
        return Response({"detail": info}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        Sign up a user

        @body email: user comment on the recipe
        @body username: user comment on the recipe
        @body password: user comment on the recipe

        @return: http status of query
        @raise HTTP_400_BAD_REQUEST: signup details must not be empty
        """

        email = get_request_body_param(request, 'email', '')
        password = get_request_body_param(request, 'password', '')
        username = get_request_body_param(request, 'username', '')

        if email == "":
            return Response({'detail': 'email must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        if username == "":
            return Response({'detail': 'username must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        if password == "":
            return Response({'detail': 'password must not be empty'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.create_user(username, email, password)
        except:
            return self.response_with_400("The username entered already exists")
        return Response({"success": True}, status=status.HTTP_201_CREATED)


class FollowUserView(APIView):

    def response_with_400(self, info):
        return Response({"detail": info}, status=status.HTTP_400_BAD_REQUEST)

    def get_userprofile(self, user_id):
        try:
            userprofile = UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            raise Http404()
        return userprofile

    def post(self, request, pk):
        """
        Follow a user with user id
        """
        current_userprofile = self.get_userprofile(request.user.id)
        to_follow_userprofile = self.get_userprofile(pk)
        try:
            current_userprofile.follows.add(pk)
        except:
            return self.response_with_400("Already followed user")
        return Response({"success": True}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """
        Unfollow a user with user id
        """
        current_userprofile = self.get_userprofile(request.user.id)
        to_unfollow_userprofile = self.get_userprofile(pk)
        if current_userprofile.follows.filter(pk=pk).exists():
            current_userprofile.follows.remove(pk)
        else:
            return self.response_with_400("Not already a follower of the target user")
        return Response({"success": True}, status=status.HTTP_200_OK)


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


# TODO: MIGHT BE ADAPTED FOR USER PROFILE SEARCH FILTERING
class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserProfileSerializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
