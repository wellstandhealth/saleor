from django.db.models.signals import post_save
from django.dispatch import receiver
from wellstand_common.wes_secrets.google_secrets import GoogleSecretManager
from wellstand_fg.api.patients_api import PatientsApi
from wellstand_fg.api_client import ApiClient
from wellstand_fg.configuration import Configuration
from wellstand_fg.models import PatientObject, LanguagePreference
from datetime import date

from saleor.account.models import User
from saleor.pharmacy.fg_auth0_api.service import FGAuth0Service
from .models import ExternalUserMapping


@receiver(post_save, sender=User)
def match_user_to_fg_patient(sender, instance, created, **kwargs):
    if not created:
        return

    existing_external_user = ExternalUserMapping.objects.filter(user=instance)
    if existing_external_user:
        return

    google_secret_manager = GoogleSecretManager()
    fg_api = google_secret_manager.get_secret("fg_api")["api"]
    token = FGAuth0Service.get_token()

    configuration = Configuration(host=fg_api, access_token=token)
    api_client = ApiClient(configuration=configuration)
    patients_api = PatientsApi(api_client=api_client)
    patients = patients_api.find_patients(email="demo@demo.com")

    if not patients:
        language_preference = LanguagePreference(code="EN", name="English")
        new_patient = PatientObject(first_name=instance.first_name,
                                    middle_name="Middle",
                                    last_name=instance.last_name,
                                    email=instance.email,
                                    primary_phone_number="00000000",
                                    alternate_phone_number="00000000",
                                    date_of_birth=date.today(),
                                    gender_assigned_at_birth="M",
                                    name_suffix="SR",
                                    language_preference=language_preference)
        created_patient = patients_api.create_patient(new_patient)
        external_id = created_patient.uuid
    else:
        external_id = patients[0].uuid

    # TODO: Create or match FG patient
    ExternalUserMapping.objects.get_or_create(
        user=instance, external_id=external_id, external_system="FG"
    )
