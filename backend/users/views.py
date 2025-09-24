from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from users.serializers import UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    renderer_classes = [JSONRenderer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.telegram_id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
