import datetime
import os

import jwt
import requests

from saleor.pharmacy.fg_api.config import FG_ISSUER, FG_AUDIENCE, FG_CLIENT_ID, \
    FG_CLIENT_SECRET


class BaseService:
    _token = None

    @staticmethod
    def _call_oauth0():
        url = FG_ISSUER + "oauth/token"
        payload = {
            "client_id": FG_CLIENT_ID,
            "client_secret": FG_CLIENT_SECRET,
            "audience": FG_AUDIENCE,
            "grant_type": "client_credentials",
        }
        response = requests.post(url, data=payload, timeout=5)
        token = response.json()["access_token"]

        with open(".fg_token", "w", encoding="utf-8") as file:
            file.write(token)

        return token

    def _get_token(self):
        token = None
        if os.path.exists(".fg_token") is False:
            return BaseService._call_oauth0()

        exp_datetime = None
        with open(".fg_token", "r", encoding="utf-8") as file:
            token = file.read()
            decoded_token = jwt.decode(token, algorithms=["HS256"],
                                       options={"verify_signature": False})
            exp_datetime = datetime.datetime.fromtimestamp(decoded_token["exp"])

        if datetime.datetime.now() > exp_datetime:
            return self._call_oauth0()

        return token

    def __init__(self):
        self._token = self._get_token()

    class Meta:
        abstract = True
