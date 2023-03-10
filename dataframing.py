import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import csv
import datetime
from PIL import Image, ImageDraw, ImageFont

def downloadProcessFiles():
    JSON_KEYFILE = 'token/cirrus-admin-dashboard-e7c8a6668840.json'
    SPREADSHEET = '【新時代】楽天進捗管理'
    WORKSHEET = '楽天ペイ顧客一覧'
    CSV_FILENAME = 'databases/楽天ペイ顧客一覧.csv'
    SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    serviceAccountCredentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEYFILE, SCOPE)
    gspreadClient = gspread.authorize(serviceAccountCredentials)
    worksheet = gspreadClient.open(SPREADSHEET).worksheet(WORKSHEET)

    with open(CSV_FILENAME, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(worksheet.get_all_values())


def downloadRecordFiles(month):
    JSON_KEYFILE = 'token/cirrus-admin-dashboard-e7c8a6668840.json'
    SPREADSHEET = '10月シフト販管インセン'
    WORKSHEET = str(month)+'月シフト'
    CSV_FILENAME = 'databases/'+str(month)+'月シフト.csv'

    SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    serviceAccountCredentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEYFILE, SCOPE)
    gspreadClient = gspread.authorize(serviceAccountCredentials)
    worksheet = gspreadClient.open(SPREADSHEET).worksheet(WORKSHEET)

    with open(CSV_FILENAME, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(worksheet.get_all_values())

def createScore(month):
    df_result = pd.DataFrame({'名前':[],'稼働時間':[],'エントリ数':[],'1次審査OK':[],'1次審査不備':[],'未着手':[],'照合なし':[],'2次審査待ち':[],'取消':[],'平均値':[],'1次審査OK平均値':[]})

    df = pd.read_csv("databases/楽天ペイ顧客一覧.csv",header=11)
    df["１次審査開始日"] = pd.to_datetime(df["１次審査開始日"],errors="coerce")
    df["エントリ日"] = pd.to_datetime(df["エントリ日"],errors="coerce")


    df["トス者"] = df["トス者"].str.replace('　',' ')

    df["トス者"] = df["トス者"].str.replace('小松みこと','小松 みこと')
    df["トス者"] = df["トス者"].str.replace('中村優太','中村 優太')
    df["トス者"] = df["トス者"].str.replace('北代竜人','北代 竜人')
    df["トス者"] = df["トス者"].str.replace('岡崎睦','岡崎 睦')

    dfmonth = df[(df['エントリ日'].dt.month == month)]

    members = dfmonth["トス者"].dropna().unique().tolist()



    ###########################################################################

    df_shift = pd.read_csv("databases/"+str(month)+"月シフト.csv" , usecols=['名前','稼働人数'])
    print(df_shift)
        
    df_shift["稼働時間"] = df_shift["稼働人数"].str.replace('　',' ')
    df_shift["名前"] = df_shift["名前"].str.replace('　',' ')
    print(df_shift["稼働時間"])

    print(df_shift)

    #メンバーリスト
    print("メンバー")
    print(members)

    #生存者
    print("シフトが発見された人")
    alive = list(set(members)&set(df_shift['名前'].tolist()))
    print(alive)
    #行方不明者リスト
    print("行方不明者")
    where = list(set(members) - set(df_shift['名前'].to_list()))
    print(where)

    print("テスト")

    ###########################################################################
    for member in alive:
        #             論理式をここに記載 
        df_mem = df[(df["トス者"]==member) & ~(df['２次審査結果'] == '申込取消') & (df['エントリ日'].dt.month == month)]

        df_mem["１次審査結果"] = df_mem["１次審査結果"].fillna("1次審査OK")

        entry_mem          = len(df[(df["トス者"]==member) & (df['エントリ日'].dt.month == month)])
        first_chk_OK       = len(df_mem[df_mem["１次審査結果"]=='1次審査OK'])
        first_chk_rack     = len(df_mem[df_mem["１次審査結果"]=='1次審査不備'])
        first_chk_untouch  = len(df_mem[df_mem["１次審査結果"]=='未着手'])
        first_chk_notFound = len(df_mem[df_mem["１次審査結果"]=='照合なし'])
        first_chk_waiting  = len(df_mem[df_mem["１次審査結果"]=='2次審査待ち'])
        
        working_time = df_shift["稼働時間"][df_shift["名前"]==member].str.replace("h","")
        working_time = df_shift["稼働時間"][df_shift["名前"]==member].str.replace("ｈ","")
        
        working_time = working_time.str.replace("時間","")
        working_time = int(working_time)
        print(working_time)
        
        try:
            avarage = entry_mem / (working_time/8)
        except ZeroDivisionError:
            avarage = 0
        
        try:
            first_chk_avarage = first_chk_OK / (working_time/8)
        except ZeroDivisionError:
            first_chk_avarage = 0


        print(avarage)
        if avarage > 40:
            avarage = 0

        second_chk_cancel = len(df[(df["トス者"]==member) & (df['２次審査結果'] == '申込取消') & (df['エントリ日'].dt.month == month)])
        df_result = df_result.append({'名前':member,'エントリ数':entry_mem,'1次審査OK':first_chk_OK,'1次審査不備':first_chk_rack,'未着手':first_chk_untouch,'照合なし':first_chk_notFound,'2次審査待ち':first_chk_waiting,'取消':second_chk_cancel,'稼働時間':working_time,'平均値':avarage,'1次審査OK平均値':first_chk_avarage},ignore_index=True)
    
    df_result1 = df_result.sort_values(by='平均値', ascending=False)
    
    real_scores = df_result.sort_values(by='エントリ数', ascending=False)
    
    df_result1 = df_result1.reset_index()
    
    real_scores = real_scores.reset_index()
    
    df_result1.to_csv("databases/"+str(month)+"月楽天ペイスコア.csv")

    scores = df_result1
    print(scores)
    print(real_scores)
    return scores, real_scores
