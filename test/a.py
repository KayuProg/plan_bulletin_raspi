from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import datetime
import urllib.parse  # URLエンコード用

# 読み取り権限を指定
SCOPES = ["https://www.googleapis.com/auth/tasks"]

json_pass = "./get_info/jsons/tasks_token.json"
service = None

def main():
    creds = None
    # トークンファイルが存在するか確認
    if os.path.exists(json_pass):
        creds = Credentials.from_authorized_user_file(json_pass, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("./get_info/jsons/parent.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open(json_pass, "w") as token:
            token.write(creds.to_json())

    try:
        global service
        service = build("tasks", "v1", credentials=creds)
        tasklists = service.tasklists().list().execute()
        tasklistid = None

        count=0
        # "Main"というタスクリストを探す
        for tasklist in tasklists["items"]:
            # print(count)
            if tasklist["title"] == "Main":
                tasklistid = tasklist["id"]
                # print(3)
            count+=1
            
    

        tasks = []
        nextpagetoken = None
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
        next_day = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"

        while True:
            response = service.tasks().list(
                tasklist=tasklistid,
                dueMax=next_day,
                showCompleted=True,
                showDeleted=False,
                showHidden=True,
                pageToken=nextpagetoken
            ).execute()

            tasks.extend(response.get("items", []))
            nextpagetoken = response.get("nextPageToken")
            if not nextpagetoken:
                break
        
        # print("\n",tasks[0],"\n")

        # 任意のタスクを選んで task_id を確認
        task_id = tasks[0].get("id") 
                
        a=service.tasks().get(tasklist=tasklistid,task=task_id).execute()
        print("\na is ",a,"\n")        

        if task_id:
            print(f"\nTask ID:{task_id}, Tasklist ID:{tasklistid}\n")
            try:
                service.tasks().patch(
                tasklist=tasklistid,
                task=task_id,
                body={"status": "completed"}  # ステータスを "completed" に設定
                ).execute()

            except HttpError as err:
                    print("error is ",err)
        else:
            print("Task ID not found.")

    except HttpError as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    main()
