import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]#アクセス権限範囲指定

json_pass="./get_info/jsons/calender_token.json"

def main():
  creds = None#認証情報を格納する変数
  if os.path.exists(json_pass):
    creds = Credentials.from_authorized_user_file(json_pass, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file("./get_info/jsons/parent.json", SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(json_pass, "w") as token:
      token.write(creds.to_json())

  try:#calenderの読み取る処理
    service = build("calendar", "v3", credentials=creds)

    #ISOformatでの日付
    now_time=datetime.datetime.utcnow()+datetime.timedelta(hours=9)
    
    now= (now_time + datetime.timedelta(days=0)).replace(hour=0, minute=0, second=0).isoformat()+"+09:00"
    next_day= (now_time + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0).isoformat()+"+09:00"
    
    #なぜか9:00以降の予定のみが反映される．
    
    
    
    # next_day= now_time.replace(hour=23, minute=59, second=59).isoformat()+"Z"
    # print(now_time)
    # print(now)
    # print(next_day)

    #now,next_dayを設定することによって本日のみのデータを返す．
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            timeMax=next_day,
            # maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    
    colors = service.colors().get().execute()#予定のカラーの辞書配列
    color_dict = colors.get('event', {})
    
    events = events_result.get("items", [])
    

    result=[]
    if events != None:#eventsがNone(その日の予定がない)時の処理．
      for event in events:
        #次の予定が含まれていたらスキップ．
        if event["start"].get("date") != None:
          continue
        #予定が次の日だと"date"がNone以外の値になるから，この条件文．
        #############################
        date=event["start"].get("dateTime", event["start"].get("date"))
        summary=event["summary"]
        color_id=event.get("colorId","1")
        color=color_dict.get(color_id, {}).get("background")
        description=event.get("description")
        
        #result配列内に辞書配列として内容を返す．
        result_con={"date":date,"summary":summary,"desc":description,"color":color}
        result.append(result_con)
  
    if not events:
      print("No upcoming events found.")
      result=[{"date":"All day","summary":"You are FREE today !!","desc":None,"color":"yellow"}]
    # print("\n",result,"\n")
    return result

  except HttpError as error:
    print(f"An error occurred: {error}")





if __name__ == "__main__":
  main()