from django.apps import AppConfig
from django.db.models.signals import post_save


class PharmacyAppConfig(AppConfig):
    name = "saleor.pharmacy"

    def ready(self):
        from saleor.account.models import User
        from .signals import match_user_to_fg_patient

        post_save.connect(
            match_user_to_fg_patient,
            sender=User,
            dispatch_uid="match_user_to_fg_patient",
        )
