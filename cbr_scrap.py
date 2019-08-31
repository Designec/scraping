from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/76.0.3809.100 Safari/537.36 OPR/63.0.3368.53'}
base_url = 'https://www.cbr.ru/currency_base/daily/?date_req=31.08.2019'


def cbr_scrap(base_url, headers):
    currency_list = []
    urls = []  # здесь будет список URL по дням
    urls.append(base_url)  # сразу же добавим в список базовый URL
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        print('All OK')
        print('----------------')
        count = 0  # просто счетчик для тестирования
        date = '31.08.2019'
        for i in range(50):
            url = f'https://www.cbr.ru/currency_base/daily/?date_req={date}'
            # берем дату, разбиваем, вычитаем один день и вставляем в URL
            day = date.split('.')
            convert_day = datetime(int(day[2]), int(day[1]), int(day[0]))
            delta_day = convert_day - timedelta(days=1)
            date = delta_day.strftime('%d.%m.%Y')
            count += 1  # все тот же стчетчик для тестирования
            print(count)
            if url not in urls:
                urls.append(url)  # добавляем URL, которых еще нет в списке

    for url in urls:
        # перебираем URL и вытаскиваем данные
        request = session.get(url, headers=headers)
        soup = BeautifulSoup(request.content, 'lxml')
        rows = soup.find_all('tr')
        for row in rows:
            try:
                cells = row.find_all('td')
                currency_list.append({
                    'Digital code': cells[0].text,
                    'Letter code': cells[1].text,
                    'Unit': cells[2].text,
                    'Currency': cells[3].text,
                    'Rate': cells[4].text,
                    'Day': url[-10:]
                })
            except:
                pass
    else:
        print('Status code: ' + str(request.status_code))  # если страница отдаст не 200 код


cbr_scrap(base_url, headers)  # работаем, братья!
