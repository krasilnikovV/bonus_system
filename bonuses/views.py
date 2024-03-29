

from rest_framework.views import APIView
from rest_framework.generics import RetrieveDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.exceptions import NotFound

from bonuses import models, serializers
from bonuses.permissions import IsOwnerOrAdmin


# Create your views here.

class UserDetailView(APIView):
    permission_classes = (IsOwnerOrAdmin,)

    def get(self, request, pk):
        user = models.User.objects.get(pk=pk)
        self.check_object_permissions(self.request, user)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)


class UserListView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        users = models.User.objects.all()
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)


class OperationIncreaseView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        serializer = serializers.OperationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(operation_type_id=1)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OperationDecreaseView(APIView):
    permission_classes = (IsOwnerOrAdmin,)

    def post(self, request):
        serializer = serializers.OperationSerializer(data=request.data)
        if serializer.is_valid():
            user = models.User.objects.get(pk=serializer.initial_data['user_id'])
            self.check_object_permissions(self.request, user)
            if user.amount_of_bonuses - serializer.validated_data['amount'] < 0:
                return Response({"detail": "Not enough bonuses"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(operation_type_id=2)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MultipleIncreaseOperationView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        serializer = serializers.MultipleIncreaseOperationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.create_operations()

            return Response(serializers.OperationSerializer(data, many=True).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OperationDetailDeleteView(RetrieveDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.OperationSerializer

    def get_object(self, pk):
        try:
            return models.Operation.objects.get(pk=pk)
        except models.Operation.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        operation = self.get_object(pk)
        serializer = serializers.OperationSerializer(operation)
        return Response(serializer.data)

    def delete(self, request, pk):
        operation = self.get_object(pk)
        operation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OperationListView(ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = models.Operation.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.OperationSerializer(queryset, many=True)
        return Response(serializer.data)
