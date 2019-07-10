from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from bonuses import models, serializers
from bonuses.permissions import IsOwner


# Create your views here.

class UserDetailView(APIView):
    permission_classes = (IsOwner, )

    def get(self, request, pk):
        user = models.User.objects.get(pk=pk)
        self.check_object_permissions(self.request, user)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)


class UserListView(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request):
        users = models.User.objects.all()
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)
