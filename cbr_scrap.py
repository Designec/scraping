from bs4 import BeautifulSoup
import requests

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/76.0.3809.100 Safari/537.36 OPR/63.0.3368.53'}
base_url = 'https://www.cbr.ru/currency_base/daily/?date_req=31.08.2019'


def cbr_scrap(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        print('Status code: ' + str(request.status_code))
        print('----------------')
        soup = BeautifulSoup(request.content, 'lxml')
    else:
        print('Status code: ' + str(request.status_code))


cbr_scrap(base_url, headers)