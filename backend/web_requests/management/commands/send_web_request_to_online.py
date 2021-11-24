import requests
import time
import json
import logging

from backend.generic.encoders import DecimalEncoder
from backend.web_requests import models as web_requests_models
from backend.branch_items import models as branch_items_models
from django.core.management.base import BaseCommand


USERNAME = "djangoadmin"
PASSWORD = "generic123"


import http.client as http_client

http_client.HTTPConnection.debuglevel = 1


def job():
    first_request = web_requests_models.WebRequest.objects.first()
    if not first_request:
        return True
    if first_request.status_code != 200 and first_request.status_code != 204:
        first_request.delete()
        return True

    BACKUP_SERVER_URL = None
    if BACKUP_SERVER_URL is None:
        local_branch_settings = branch_items_models.LocalBranchSettings.objects.first()
        if not local_branch_settings:
            return True

        BACKUP_SERVER_URL = local_branch_settings.backup_server_url

    logging.basicConfig(format="%(asctime)s %(message)s")
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

    with requests.Session() as session:
        # get access token
        access_token = None
        url = "%s/v1/tokens/acquire/" % BACKUP_SERVER_URL
        try:
            headers = {
                "Content-type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
            }
            response = session.post(
                url,
                data=json.dumps(
                    {
                        "username": USERNAME,
                        "password": PASSWORD,
                    },
                    cls=DecimalEncoder,
                ),
                headers=headers,
                timeout=5,
            )

            time.sleep(5)
            response.raise_for_status()

            response_dict = json.loads(response.text)

            access_token = response_dict["access"]
        except Exception as e:
            print("Failed to get access token", str(e))
            return True

        # send the request online
        url = "%s%s" % (BACKUP_SERVER_URL, first_request.path)
        headers = {
            "Content-type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
            "Authorization": f"Bearer {access_token}",
        }
        try:
            if first_request.method == "POST":
                response = session.post(
                    url, data=json.loads(first_request.post), headers=headers
                )
            elif first_request.method == "PATCH":
                response = session.patch(
                    url, data=json.loads(first_request.post), headers=headers
                )
            elif first_request.method == "DELETE":
                response = session.delete(url, headers=headers)

            time.sleep(5)
            response.raise_for_status()

            print("Successfully sent request", str(first_request.path))
            first_request.delete()
        except Exception as e:
            print("Failed to send request", str(e))
            return True

    return True


class Command(BaseCommand):
    def handle(self, *args, **options):
        job()
