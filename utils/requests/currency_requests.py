from utils.requests.api.requests import ExternalReq


class CurrencyRequest(ExternalReq):
    @staticmethod
    async def get_mono_curr() -> list:
        url = 'https://api.monobank.ua/bank/currency'
        return await CurrencyRequest.make_request(url)
