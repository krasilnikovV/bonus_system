import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    amount_of_bonuses = models.DecimalField(max_digits=13, decimal_places=0, default=0)


class Operation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False, blank=False, unique=True)
    user = models.ForeignKey('User',
                             on_delete=models.CASCADE,
                             related_name='operations',
                             blank=False,
                             null=False,
                             db_index=True,
                             editable=False)
    amount = models.DecimalField(max_digits=13, decimal_places=0, default=0, blank=False, null=False)
    operation_type = models.ForeignKey('OperationTypes', on_delete=models.PROTECT, blank=False, null=False)

    def __str__(self):
        return 'Operation id : %s' % self.id.__str__()


class OperationTypes(models.Model):
    type = models.CharField(max_length=32, blank=False, null=False)

    def __str__(self):
        return self.type.__str__()
