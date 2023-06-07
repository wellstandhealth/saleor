from django.db.models.signals import post_save
from django.dispatch import receiver

from saleor.account.models import User
from .models import ExternalUserMapping


@receiver(post_save, sender=User)
def match_user_to_fg_patient(sender, instance, **kwargs):
    # TODO: Create or match FG patient
    ExternalUserMapping.objects.get_or_create(
        user=instance, external_id="TODO", external_system="FG"
    )
