import requests
import json
import sys

get_contact_url = "https://api.chatwork.com/v2/contacts" 

def getContacts(API_KEY):
    global get_contact_url

    headers = {'X-ChatWorkToken': API_KEY}
    data = requests.get(get_contact_url,headers=headers)
    dict_data = json.loads(data.content)
    print(dict_data)
    print(json.dumps(dict_data, indent=2,ensure_ascii=False))

def getAllRoomId(API_KEY):
    global get_contact_url
    roomid_list = []

    headers = {'X-ChatWorkToken': API_KEY}

    data = requests.get(get_contact_url,headers=headers)
    dict_data = json.loads(data.content)
    print(dict_data)
    print(json.dumps(dict_data, indent=2,ensure_ascii=False))

    for key in range(len(dict_data)):
        roomid_list.append(dict_data[key]["room_id"])

    return roomid_list

