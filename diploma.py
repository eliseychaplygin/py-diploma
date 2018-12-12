import requests
from pprint import pprint

TOKEN = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'
APP_ID = 6773586
URL_API = 'https://api.vk.com/method/'
user_id = '171691064'

def get_friends_list(user_id):
    params = {
        'access_token': TOKEN,
        'v': '5.92',
        'user_id': user_id
    }
    resp = requests.get(URL_API + 'friends.get', params=params)
    friends = resp.json()
    friends_list = friends['response']['items']
    return friends_list

def get_groups(user_id):
    params = {
        'access_token': TOKEN,
        'v': '5.92',
        'user_id': user_id
    }
    resp = requests.get(URL_API + 'groups.get', params=params)
    groups = resp.json()
    groups_list = groups['response']['items']
    return groups_list

user_group_list = get_groups(user_id)
user_friends_list = get_friends_list(user_id)

def get_friends_groups(friends_list):
    group_friend_list = []
    count = 0
    for friend_id in friends_list:
        params = {
            'access_token': TOKEN,
            'v': '5.92',
            'user_id': friend_id
        }
        # print('.', end=' ')
        resp = requests.get(URL_API + 'groups.get', params=params)
        group = resp.json()
        try:
            for i in group['response']['items']:
                group_friend_list.append(i)
        except KeyError:
            count += 1 #просто для интереса
    set(group_friend_list)
    return list(group_friend_list)


def comparison_group(user_group_list, group_friends_list):
    res_list = []
    for group_id in user_group_list:
        if group_id not in group_friends_list:
            res_list.append(group_id)
    return print(res_list)

friends_group =[4100014, 22798006, 32439535, 14785431, 41139501, 49298257, 167597091, 101125438, 52260507, 5606643, 40282573, 26424819, 129878488, 58303964, 26310332, 109700925, 5409517, 98032777, 72633813, 117779568, 63228590, 144218281, 9156679, 43650750, 11597467, 116261992, 145809034, 64043104, 129594987, 53684863, 161434380, 88996895, 13881742, 134326172, 84861282, 14921225, 88036767, 55735037, 73112596, 73821979, 40632615, 144768584, 85691389, 22958775, 65987412, 136689834, 109232994, 94280911, 125107285, 73651226] #get_friends_groups(user_friends_list)
user_group = [8564, 125927592, 101522128, 4100014, 35486626, 27683540, 151498735, 142410745]
comparison_group(user_group, user_friends_list)
