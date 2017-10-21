from rest_framework import status
from rest_framework.exceptions import APIException


class NotAuthorized(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Not found.'
    default_code = 'not_found'
