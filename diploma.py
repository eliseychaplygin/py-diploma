import requests
import json
import time
from pprint import pprint


def get_token():
    token = ''
    with open('data.json') as file:
        json_data = json.load(file)
        for key, value in json_data.items():
            if key == 'TOKEN':
                token = value
        return token


def get_friends_list(user_id, params):
    params['user_id'] = user_id
    resp = requests.get(URL_API + 'friends.get', params=params)
    friends = resp.json()
    friends_list = friends['response']['items']
    return friends_list

def get_groups(user_id, params):
    params['user_id'] = user_id
    resp = requests.get(URL_API + 'groups.get', params=params)
    groups = resp.json()
    groups_list = groups['response']['items']
    return groups_list

def get_friends_groups(friends_list, params):
    group_friend_list = []
    count = 1
    for friend_id in friends_list:
        params['user_id'] = friend_id
        resp = requests.get(URL_API + 'groups.get', params=params)
        print(f'Собираем информацию по сообществам среди друзей. Обрабатываем {count} друга из {len(friends_list)}')
        group = resp.json()
        try:
            for i in group['response']['items']:
                group_friend_list.append(i)
        except KeyError:
            if 7 == group['error']['error_code']:
                print('Пользователь закрыл информацию по своим сообществам')
            elif 6 == group['error']['error_code']:
                print('Превышено количество запросов в секунду')
            elif 18 == group['error']['error_code']:
                print('Страница удалена или заблокирована')
            elif 30 == group['error']['error_code']:
                print('Страница приватная')
            else:
                print(f'Возникла ошибка № {group["error"]["error_code"]}')
        count += 1
        time.sleep(3)
    set(group_friend_list)
    return list(group_friend_list)


def comparison_group(user_group_list, group_friends_list):
    res_list = list(set(user_group_list) - set(group_friends_list))
    return res_list

def get_group_info(group_list, params):
    info_list = []
    info_group_list = []
    info_group_dict = {}
    for group in group_list:
        params['group_ids'] = group
        params['fields'] = 'members_count'
        resp = requests.get(URL_API + 'groups.getById', params=params).json()
        info_list.append(resp['response'][0])
    for i in info_list:
        for key, value in i.items():
            if 'name' == key:
                info_group_dict[key] = value
            elif 'id' == key:
                info_group_dict['gid'] = value
            elif 'members_count' == key:
                info_group_dict[key] = value
        info_group_list.append(info_group_dict.copy())
    return info_group_list

def write_json(info):
    with open('groups.json', 'w') as f:
        json.dump(info, f, indent=4)



if __name__ == '__main__':
    URL_API = 'https://api.vk.com/method/'
    user_id = '171691064'
    token = get_token()
    params = {
        'access_token': token,
        'v': '5.92'
    }
    user_group_list = get_groups(user_id, params)
    user_friends_list = get_friends_list(user_id, params)
    group_friends_list = get_friends_groups(user_friends_list, params)
    unique_group = comparison_group(user_group_list, group_friends_list)
    group_info = get_group_info(unique_group, params)
    write_json(group_info)