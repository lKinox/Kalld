import everapi


class Client(everapi.Client):
    def __init__(self, api_key, base='https://api.numlookupapi.com/v1'):
        super(Client, self).__init__(base, api_key)

    def status(self):
        return self._request('/status')

    def validate(self, phone_number, country_code=None):
        return self._request(f'/validate/{phone_number}', params={
            'country_code': country_code
        })
