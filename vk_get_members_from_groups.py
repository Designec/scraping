# Получаем участников одной или нескольких групп, убираем дубликаты, которые сидят и там и там
# Сохраняем это все в обычные текстовые файлы
import requests

groups = ['python_community', 'we_use_django']  # можно прописать одну или несколько групп
users = []  # сюда будем скидывать найденные id юзеров
users_double = []  # а это для дублей на всякий случай

for group in groups:
    # token берется в настройках приложения API vk, вам нужно получить свой токен
    token = '05ebb9ea05ebb9ea05ebb9ea9205871aca005eb05ebb9ea5880d0b76f8aed411b4c100b'
    version = 5.101  # последняя актуальная версия API vk
    count = 1000  # за раз vk отдает не больше 1000 юзеров
    offset = 0  # смещение

    # узнаем для начала количество участников сообщества
    response = requests.get('https://api.vk.com/method/groups.getMembers',
                            params={'access_token': token, 'group_id': group, 'v': version})
    count_users = response.json()['response']['count']

    # теперь в цикле получим, переберем по 1000 участников и добавим найденных к списку users
    while offset < count_users:
        response = requests.get('https://api.vk.com/method/groups.getMembers',
                                params={
                                    'access_token': token,
                                    'group_id': group,
                                    'v': version,
                                    'count': count,
                                    'offset': offset
                                })
        data_users = response.json()['response']['items']  # получаем сразу id пользователей

        for data in data_users:
            if data not in users:
                users.append(data)
            else:
                users_double.append(data)  # скидываем сюда дубли... на всякий случай
        offset += 1000  # смещаем

all_double = len(users_double)  # посчитаем сколько всего дублей
users_double = set(users_double)  # а теперь удалим дубли дублей


# сохраняем в обычный текстовый файл уникальных участников из всех групп
def save_to_file(self):
    with open('users_db.txt', 'w', encoding='utf-8') as f:
        for user in users:
            f.write('https://vk.com/id' + str(user) + '\n')


# сохраняем в файл дубли... на всякий случай
def double_to_file(self):
    with open('users_double_db.txt', 'w', encoding='utf-8') as f:
        for double in users_double:
            f.write('https://vk.com/id' + str(double) + '\n')


# сохраняем, братья!
save_to_file(users)
double_to_file(users_double)

print('--------------')
print('Уникальных участников: ' + str(len(users)) + ' (сохранено в users_db.txt)')
print('Дубликаты: ' + str(len(users_double)) + '/' + str(all_double) + ' (сохранено в users_double_db.txt)')
print('--------------')
print('Finita la commedia')
