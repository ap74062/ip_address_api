import requests


class IPStackApi:
    def __init__(self, api_access_key: str):
        self.url = "http://api.ipstack.com/{}"
        self.api_access_key = api_access_key

    def __make_request(self, ip_address: str) -> requests.Response:
        r = requests.get(self.url.format(ip_address),
                         params={'access_key': self.api_access_key})

        print(r.json())
        if r.status_code != 200:
            raise Exception('Error while connecting to api: {}, {}'
                            .format(r.status_code, r.text))
        return r

    def get(self, ip_address: str):
        response = self.__make_request(ip_address)
        return response.json()
