import os
import requests
from dotenv import load_dotenv


load_dotenv('.env')


class DataService:

    def __init__(self):
        self.__baseurl = os.getenv('API', 'invalid-url')

    def get_sku_data(self, navigation):
        response = requests.get(
            url=f'{self.__baseurl}{navigation}',
            timeout=10
        )
        return response.json()['results']
