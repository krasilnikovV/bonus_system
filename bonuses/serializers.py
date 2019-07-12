from rest_framework import serializers
from bonuses import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'amount_of_bonuses')


class OperationSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=13, decimal_places=0)
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Operation
        fields = ('user', 'user_id', 'amount', 'operation_type')
        depth = 1
