from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get("access_token")

        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token["user_id"]
                request.user = get_user_model().objects.get(id=user_id)
            except:
                request.user = None

        return self.get_response(request)