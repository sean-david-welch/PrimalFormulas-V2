import json

from utils.config import settings
from firebase_admin import credentials, initialize_app

service_account_info = settings["SERVICE_ACCOUNT_STRING"]

if service_account_info is not None:
    service_account_json = json.loads(service_account_info)

    cred = credentials.Certificate(service_account_json)
    initialize_app(cred)
else:
    print("environment variable not found.")
