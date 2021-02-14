from rest_framework import authentication
from rest_framework import status
from rest_framework.exceptions import APIException

from restaurant.models import User


class NoAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "No authentication token provided"
    default_code = "no_auth_token"


class LoginAuthentication(authentication.BaseAuthentication):

    def authenticate_header(self, request):
        return 'login'

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header:
            raise NoAuthToken("No auth token provided")

        login = auth_header.split(" ").pop()

        user, created = User.objects.get_or_create(username=login)

        return (user, f'{login}')
