# Парсим сайт центробанка РФ и получаем курсы валют за указанное время (по умолчанию последние 30 дней)
# полученные данные сохраняем в csv файл
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import requests
import csv

start_time = datetime.now()
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/76.0.3809.100 Safari/537.36 OPR/63.0.3368.53'}

url_date = datetime.now().strftime('%d.%m.%Y')
base_url = 'https://www.cbr.ru/currency_base/daily/?date_req=' + url_date
currency_list = []
urls = []
target_date = '08.08.2019'

def cbr_scrap(base_url, headers):
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        print('Отлично, работаем дальше')
        print('----------------')
        count = 0  # будем считать дни
        date = url_date
        while date != target_date:  # собираются данные до определенной даты target_date
            url = f'https://www.cbr.ru/currency_base/daily/?date_req={date}'
            # берем дату, разбиваем, придаем вид [31, 8, 2019], вычитаем один день и вставляем в URL
            # криво, но пока не нзнаю как сделать лучше
            split_date = date.split('.')
            convert_date = datetime(int(split_date[2]), int(split_date[1]), int(split_date[0]))
            delta_date = convert_date - timedelta(days=1)
            date = delta_date.strftime('%d.%m.%Y')
            count += 1
            if url not in urls:
                urls.append(url)
    else:
        print('Status code: ' + str(request.status_code))  # узнаем какой код отдаст страница, если не 200

    print('Получено страниц для обработки: ' + str(len(urls)))
    print('Приступаем к извлечению данных...')

    for url in urls:
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
                    'Date': url[-10:]
                })
            except:
                pass
    return currency_list


def save_to_file(currency_list):
    with open('currency_db.csv', 'w', newline='', encoding='utf-8') as f:
        data_temp = csv.writer(f)
        data_temp.writerow(('Цифровой код', 'Буквенный код', 'Единица',
                            'Валюта', 'Курс', 'Дата'))
        for curr in currency_list:
            data_temp.writerow((curr['Digital code'],
                                curr['Letter code'],
                                curr['Unit'],
                                curr['Currency'],
                                curr['Rate'],
                                curr['Date']
                                ))


# работаем, братья!
currency_list = cbr_scrap(base_url, headers)

print('Данные успешно извлечены, сохраняем...')

save_to_file(currency_list)
finish_time = (datetime.now() - start_time)


print('Полученные данные сохранены в currency_db.csv')
print('----------------')
print('Время:', finish_time)
