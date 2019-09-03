# Получаем друзей определенного пользователя. Если указан id пользователя, то ищем по нему
# если id не указан, то ищем по короткому имени пользователя user_domain
import requests

# token берется в настройках приложения API vk, вам нужно получить свой токен
token = '05ebb9ea05ebb9ea05ebb9ea9205871aca005eb05ebb9ea5880d0b76f8aed411b4c100b'
version = 5.101
count = 5000  # за раз vk отдает не больше 5000 друзей
offset = 0  # смещение
user_domain = ['idesignec']  # короткое имя нужног овам человека
user_id = []  # id пользователя
friends = []  # сюда будем скидывать найденные id друзей

# если задано короткое имя пользователя user_domain и пустой user_id, то сначала посылается запрос,
# чтобы получить id пользователя по этому имени
# если user_id не пустой, то сразу ищется по нему
if not user_id:
    response = requests.get('https://api.vk.com/method/users.get',
                            params={'access_token': token, 'user_ids': user_domain, 'v': version})
    response_list = response.json()['response']
    id = response_list[0]['id']
else:
    id = user_id


# узнаем для начала количество друзей
response = requests.get('https://api.vk.com/method/friends.get',
                        params={'access_token': token, 'user_id': id, 'v': version})
count_friends = response.json()['response']['count']

# теперь в цикле получаем по 5000 друзей и добавляем найденных к списку friends
while offset < count_friends:
    response = requests.get('https://api.vk.com/method/friends.get',
                            params={
                                'access_token': token,
                                'user_id': id,
                                'v': version,
                                'count': count,
                                'offset': offset
                            })
    data_friends = response.json()['response']['items']  # получаем id 5000 друзей
    friends.extend(data_friends)  # расширяем список путем добавления новых данных
    offset += 5000  # смещаем


# все посчитали, теперь надо бы это сохранить в файл
def save_to_file(friends):
    with open('friends_db.txt', 'w', encoding='utf-8') as f:
        for friend in friends:
            f.write('https://vk.com/id' + str(friend) + '\n')


save_to_file(friends)  # сохраняем

print('Количество друзей: ' + str(len(friends)))
print('сохранено в friends_db.txt')
print('--------------')
print('Finita la commedia')