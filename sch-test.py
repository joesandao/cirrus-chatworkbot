import schedule
from time import sleep
from datetime import datetime,date

#01 定期実行する関数を準備
def task():
    print("タスク実行中")
    
#02 スケジュール登録
schedule.every(30).seconds.do(task)

#02 何時まで実行するか定義
year   = date.today().year
month  = date.today().month
hour   = 22
minute = 0
second = 0
set_until_time = datetime(year,month,date.today().day,hour,minute,second)

#03 イベント実行 (特定の時間が来るまで定期実行)
while datetime.now() < set_until_time:
    schedule.run_pending()
    sleep(1)
