import requests
def sendMessage(BASE_URL,API_KEY,message):
    roomid   = '297650520' #ルームIDを記載
    post_message_url = '{}/rooms/{}/messages'.format(BASE_URL, roomid)

    headers = { 'X-ChatWorkToken': API_KEY}
    params = { 'body': message }
    requests.post(post_message_url, headers=headers, params=params)

def sendFile(API_KEY,file_path,roomid,message):
    file_name = "ランキング表.pdf"
    

    file_data = open(file_path, 'rb').read()
    files = {
        "file": (file_name, file_data, "text/plain"),
    }
    data = {
        "message": message
    }
    post_message_url = 'https://api.chatwork.com/v2/rooms/{}/files'.format(roomid)
    headers = {'X-ChatWorkToken': API_KEY}
    response = requests.post(
        post_message_url,
        headers=headers,
        files=files,
        data=data,
    )
