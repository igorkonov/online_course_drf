from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from users.models import User
from users.permissions import IsUserProfile
from users.serializers import UserSerializer, AuthUserSerializer, PaymentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AuthUserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action in ['update', 'partial_update']:
            permission_classes = [IsUserProfile]
        if self.action in ['create']:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        if self.request.user == self.get_object() or self.request.user.is_superuser:
            serializer_class = UserSerializer
        else:
            serializer_class = AuthUserSerializer
        serializer = serializer_class(self.get_object())
        serializer_data = serializer.data
        #serializer_data['payment'] = PaymentSerializer(self.get_object().payment_set.all(), many=True).data
        return Response(serializer_data)
