import datetime
import os

import jwt
import requests

from saleor.pharmacy.fg_auth0_api.config import FG_ISSUER, FG_AUDIENCE, FG_CLIENT_ID, \
    FG_CLIENT_SECRET


class FGAuth0Service:
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

    @staticmethod
    def get_token():
        token = None
        if os.path.exists(".fg_token") is False:
            return FGAuth0Service._call_oauth0()

        exp_datetime = None
        with open(".fg_token", "r", encoding="utf-8") as file:
            token = file.read()
            decoded_token = jwt.decode(token, algorithms=["HS256"],
                                       options={"verify_signature": False})
            exp_datetime = datetime.datetime.fromtimestamp(decoded_token["exp"])

        if datetime.datetime.now() > exp_datetime:
            return FGAuth0Service._call_oauth0()

        return token
