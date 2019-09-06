# Скачиваем все фотографии из определенного альбома сообщества ВКонтакте
# 'album-67785094_190843526' первая группа цифр вместе с '-' это id владельца альбома
# вторая группа цифр это id альбома откуда нужно скачать фото
import wget
import requests

token = 'your access token'
version = 5.101
count = 1000  # vk api за раз отдает не больше 1000
offset = 0
owner_id = -67785094
album_id = '190843526'
data_album = []  # сюда скинем все поулченные данные
url_photos = []  # здесь будут ссылки на фото

response = requests.get('https://api.vk.com/method/photos.get',
                            params={'access_token': token, 'owner_id': owner_id,
                                    'album_id': album_id, 'v': version, 'count': count})
photo_count = response.json()['response']['count']


# в цикле запрашиваем, получаем ответ и скидываем в data_album
while offset < photo_count:
    response = requests.get('https://api.vk.com/method/photos.get',
                            params={
                                    'access_token': token,
                                    'owner_id': owner_id,
                                    'album_id': album_id,
                                    'v': version,
                                    'count': count,
                                    'offset': offset
                            })
    data_album.extend(response.json()['response']['items'])
    offset += 1000  # смещаем

# перебираем спсок с данными, выдергиваем от туда ссылки на самые большие размеры фото
# и скачиваем их в папку со скриптом
for i in range(photo_count):
    url = data_album[i]['sizes'][-1]['url']
    print(url)
    wget.download(url)
    url_photos.append(url)

print('All ' + str(len(url_photos)) + ' photos downloaded')
