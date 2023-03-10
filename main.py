from setproctitle import setproctitle,getproctitle
import datetime
import dataframing as frame
import chatworkPost as chat
import getContacts as getcnt
import createRanking 
import schedule
from time import sleep
import createRealRanking

today = datetime.today()
setproctitle("chatwork-bot")

def main():
    try:
        frame.downloadProcessFiles()
    except:
        print("進捗シートをダウンロードできませんでした。")

    try:
        frame.downloadRecordFiles(11) #その月のシフト表をダウンロードする
    except:
        print("シフトシートをダウンロードできませんでした。")
    

    BASE_URL = 'https://api.chatwork.com/v2'
    API_KEY  = '4002b12717981aa8cf02764a3dd5892d' 
    message  = ""

    '''
    chat.sendMessage(BASE_URL,API_KEY,message)
    chat.sendFile(API_KEY)
    a = getcnt.getAllRoomId(API_KEY)
    print(a)
    '''

    a , b = frame.createScore(today.month)

    createRanking.write1to3(a)
    createRanking.title_link_1to3()
    createRanking.dfPlt(a)
    createRanking.head_link_4toend()
    createRanking.imgtopdf()
    
    createRealRanking.write1to3(b)
    createRealRanking.title_link_1to3()
    createRealRanking.dfPlt(b)
    createRealRanking.head_link_4toend()
    createRealRanking.imgtopdf()

    
    chat.sendFile(API_KEY,"all.pdf","280102567","[手動配信]アポイント平均値ランキング")
    chat.sendFile(API_KEY,"all_real.pdf","280102567","[手動配信]アポイント絶対値ランキング")
    
schedule.every().monday.at("09:00").do(main)
schedule.every().tuesday.at("09:00").do(main)
schedule.every().wednesday.at("09:00").do(main)
schedule.every().thursday.at("09:00").do(main)
schedule.every().friday.at("09:00").do(main)
schedule.every().saturday.at("09:00").do(main)

while True:
    schedule.run_pending()
    sleep(1)
    main()

main()
