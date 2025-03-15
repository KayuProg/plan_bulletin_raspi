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
    now = now_time.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"  # 'Z' indicates UTC time
    next_day= (now_time + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()+"Z"

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
    
    
    if not events:
      print("No upcoming events found.")
      return 

    result=[]
    for event in events:
      date=event["start"].get("dateTime", event["start"].get("date"))
      summary=event["summary"]
      color_id=event.get("colorId","1")
      color=color_dict.get(color_id, {}).get("background")
      description=event.get("description")
      
      #result配列内に辞書配列として内容を返す．
      result_con={"date":date,"summary":summary,"desc":description,"color":color}
      result.append(result_con)
      
      
    return result

  except HttpError as error:
    print(f"An error occurred: {error}")





if __name__ == "__main__":
  main()