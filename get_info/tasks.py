# -*-coding: utf-8 -*-
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import datetime
import traceback
import time

# 読み取り権限を指定
SCOPES = ["https://www.googleapis.com/auth/tasks"]
#うまく実行されないとき
#google.auth.exceptions.RefreshError: ('invalid_scope: Bad Request', {'error': 'invalid_scope', 'error_description': 'Bad Request'})
#というエラーが出たとき次のやつで実行するとよさそう．
# SCOPES = ["https://www.googleapis.com/auth/tasks.readonly"]


json_pass="./get_info/jsons/tasks_token.json"

service=None
tasklistid=None


def main():
    creds = None#認証情報を格納する変数
    # トークンファイルを確認して認証情報をロード
    if os.path.exists(json_pass):#.jsonが存在するかの確認
        creds = Credentials.from_authorized_user_file(json_pass, SCOPES)
    
    # 認証情報が無効な場合、ログインプロセスを実行
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:#tokenの期限切れ確認
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("./get_info/jsons/parent.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open(json_pass, "w") as token:
            token.write(creds.to_json())


    #######################################################
    #実際に情報を取得する
    #######################################################    
    try:
        global service
        service = build("tasks", "v1", credentials=creds)
        tasklists = service.tasklists().list().execute()
        global tasklistid
        for tasklist in tasklists["items"]:
            # print(tasklist)
            if tasklist["title"] == "Main":
                tasklistid = tasklist["id"]
        # print("Task List ID is ",tasklistid)
    
            
        tasks = []
        nextpagetoken = None
        
        now=datetime.datetime.utcnow()+datetime.timedelta(hours=9)#時刻の補正は行わない．本来はhours=9
        today =now.replace(hour=0,minute=0,second=0, microsecond=0).isoformat() + "Z"  # 'Z' indicates UTC time
        next_day= (now + datetime.timedelta(days=1)).replace(hour=0,minute=0,second=0, microsecond=0).isoformat()+"Z"

        
        while True:
            response = (
                service.tasks()
                .list(
                    tasklist=tasklistid,
                    # dueMin=today,
                    dueMax=next_day,#今日までのタスクを取得する．
                    showCompleted=True,
                    showDeleted=False,
                    showHidden=True,
                    # maxResults=100,
                    pageToken=nextpagetoken,
                )
                .execute()
            )
            tasks.extend(response.get("items"))
            nextpagetoken = response.get("nextPageToken")
            if not nextpagetoken:
                break
        
        display_tasks=[]
        for task in tasks:
            task_info=[]#taskの情報を格納する．
            title=task.get("title")
            note=task.get("notes")
            status=task.get("status")
            due=task.get("due")
            due_check="not_expired"#期限が切れていたら"expired"，切れていなかったら"not expired"と表示する．due_dateとtoday_dateの比較文の関係から初期値をexpireに設定
            task_id=task.get("id") #ボタンでcompletedとかを変更するためのid
            
            due_date=datetime.datetime.fromisoformat(due).strftime("%m-%d")
            today_date=datetime.datetime.fromisoformat(today).strftime("%m-%d")
            if due_date != today_date:#今日以外のtaskはexpired
                # print(due_date,"   ",today_date)
                due_check="expired"
            task_info={"title":title,"note":note,"status":status,"due":due,"due_check":due_check,"tasklist_id":tasklistid,"task_id":task_id}
            
            display_tasks.append(task_info)
            #print(task.get("title")," \n")
        
        # print(display_tasks)

        return display_tasks
            
            
    except HttpError as err:
        print(err)
        
        
        
        
        
        
def change_status(task_id,status,btn_value):
    # print(tasklist_id)
    print(f"\nTasklist ID: {tasklistid},Task ID:{task_id} Status: {status}, Checked: {btn_value}\n")
    
    if btn_value:
        overwrite_status="completed"
    else :
        overwrite_status="needsAction"
        
    #成功するまで処理繰り返す    
    
    time.sleep(3)
    
    for _ in range(3):  # 最大3回実行
        try:
            service.tasks().patch(
                            tasklist=tasklistid,
                            task=task_id,
                            body={"status": f"{overwrite_status}"}
                        ).execute()
        except Exception as e:
            print("失敗しました。もう一度繰り返します", _)
            print(traceback.format_exc()) # 例外の内容を表示
            time.sleep(1) # 適当に待つ
        else:
            print("成功しました。ループを終了します。")
            break
    else:
        print("最大試行回数に達しました。処理を中断します")
        # raise <適当なエラー>
        
    
    return 0
    
    
    
    
if __name__ == "__main__":
    main()

