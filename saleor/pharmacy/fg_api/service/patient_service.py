import requests

from saleor.pharmacy.fg_api.config import FG_API_BASE_URL
from saleor.pharmacy.fg_api.data import PatientData
from saleor.pharmacy.fg_api.service.base_service import BaseService


class PatientService(BaseService):
    _END_POINT = "patients/1/"

    def get_patient_by_uuid(self, patient_uuid):
        url = f"{FG_API_BASE_URL}{self._END_POINT}{patient_uuid}"
        headers = {"Authorization": f"Bearer {self._token}"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        return PatientData.build(data)
