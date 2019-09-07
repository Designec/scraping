# Получаем подписчиков определенного пользователя. Если указан id пользователя, то ищем по нему
# если id не указан, то ищем по короткому имени пользователя user_domain
import requests

# token берется в настройках приложения API vk, вам нужно получить свой токен
token = '05ebb9ea05ebb9ea05ebb9ea9205871aca005eb05ebb9ea5880d0b76f8aed411b4c100b'
version = 5.101
count = 1000  # за раз vk отдает не больше 1000 подписчиков
offset = 0
user_domain = ['idesignec']  # короткое имя
user_id = ['406774428']  # id пользователя
followers = []

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


# узнаем для начала количество подписчиков
response = requests.get('https://api.vk.com/method/users.getFollowers',
                        params={'access_token': token, 'user_id': id, 'v': version})
count_followers = response.json()['response']['count']

# теперь в цикле получаем по 1000 подписчиков и добавляем найденных к списку followers
while offset < count_followers:
    response = requests.get('https://api.vk.com/method/users.getFollowers',
                            params={
                                'access_token': token,
                                'user_id': id,
                                'v': version,
                                'count': count,
                                'offset': offset
                            })
    data_followers = response.json()['response']['items']
    followers.extend(data_followers)
    offset += 1000


# все посчитали, теперь надо бы это сохранить в файл
def save_to_file(followers):
    with open('followers_db.txt', 'w', encoding='utf-8') as f:
        for follower in followers:
            f.write('https://vk.com/id' + str(follower) + '\n')


save_to_file(followers)  # сохраняем

print('Количество подписчиков: ' + str(len(followers)))
print('сохранено в followers_db.txt')
print('--------------')
print('Finita la commedia')
