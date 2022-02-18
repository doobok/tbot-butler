import json

import requests


class ExternalReq:
    @staticmethod
    async def make_request(
            url: str
    ):
        result = requests.get(url)
        if result.status_code == 200:
            try:
                result = result.json()
            except json.decoder.JSONDecodeError:
                result = False
            return result
        else:
            return False
