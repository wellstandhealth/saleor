import uuid
from django.db import models

from saleor.account.models import User


class BaseAuditMixin(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        db_column="uuid",
        unique=True,
    )
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class ExternalUserMapping(BaseAuditMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=255, db_index=True)
    external_system = models.CharField(max_length=25)
