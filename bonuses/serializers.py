from rest_framework import serializers
from bonuses import models, validators


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'amount_of_bonuses')


class OperationSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=13, decimal_places=0)
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    expiration_date = serializers.DateField(default=None,
                                            allow_null=True,
                                            validators=[validators.not_earlier_today_validator])

    class Meta:
        model = models.Operation
        fields = ('user', 'user_id', 'amount', 'operation_type', 'expiration_date')
        depth = 1


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class MultipleIncreaseOperationSerializer(serializers.Serializer):
    user_ids = IdSerializer(many=True, write_only=True)
    users = UserSerializer(many=True, read_only=True)
    amount = serializers.DecimalField(max_digits=13, decimal_places=0, allow_null=False)
    expiration_date = serializers.DateField(default=None,
                                            allow_null=True,
                                            validators=[validators.not_earlier_today_validator])

    def __create_operation__(self, data):
        serializer = OperationSerializer(data=data)
        if serializer.is_valid():
            return serializer.save(operation_type_id=1)

    def create_operations(self):
        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.create_operations()`.'
        )

        assert not self.errors, (
            'You cannot call `.create_operations()` on a serializer with invalid data.'
        )

        amount = self.validated_data['amount']
        expiration_date = self.validated_data['expiration_date']
        user_ids = self.validated_data['user_ids']
        operations = []
        for user_id in user_ids:
            data = {
                "user_id": user_id.get('id'),
                "amount": amount.__str__(),
                "expiration_date": expiration_date.__str__()
            }
            operations.append(self.__create_operation__(data=data))
        return operations

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError
