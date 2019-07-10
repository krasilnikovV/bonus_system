from rest_framework import serializers
from bonuses.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'amount_of_bonuses')
