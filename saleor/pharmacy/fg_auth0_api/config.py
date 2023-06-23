from wellstand_common.wes_secrets.google_secrets import GoogleSecretManager

google_secret_manager = GoogleSecretManager()
fg_config = google_secret_manager.get_secret("fg_auth0")

FG_ISSUER = fg_config["issuer"]
FG_AUDIENCE = fg_config["audience"]
FG_CLIENT_ID = fg_config["client_id"]
FG_CLIENT_SECRET = fg_config["client_secret"]
