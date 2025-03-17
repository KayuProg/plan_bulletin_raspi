import flet as ft
import datetime

#実行場所によるので注意
import get_info.calender as calender

class calender_contents():
    def __init__(self):
        super().__init__()
        
        ####################### main bar ########################
        
        #TODOディスプレイのサイズに合わせて文字の大きさも変わるようにしたいね．
        # self.title=ft.Stack(ft.Text(spans=[ft.TextSpan("Tosay's schedule", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,weight=ft.FontWeight.W_500,color="black"))],
        #                     ft.Text("Tosay's schedule", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,weight=ft.FontWeight.W_800,color="white"),)
        
        self.title= ft.Stack(
            [
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "Today's schedule",
                            ft.TextStyle(
                                size=45,
                                weight=ft.FontWeight.BOLD,
                                foreground=ft.Paint(
                                    color="black",
                                    stroke_width=3,
                                    stroke_join=ft.StrokeJoin.ROUND,
                                    style=ft.PaintingStyle.STROKE,
                                ),
                            ),
                        ),
                    ],
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "Today's schedule",
                            ft.TextStyle(
                                size=45,
                                weight=ft.FontWeight.BOLD,
                                color="white",
                            ),
                        ),
                    ],
                ),
            ]
        )
        
        self.title_container=ft.Container(content=self.title,alignment=ft.alignment.center)#containerを使ってTitleを中央配置
        
        # self.back_date=ft.IconButton(icon=ft.icons.ARROW_CIRCLE_LEFT, on_click=self.back_date_func)
        # self.forward_date=ft.IconButton(icon=ft.icons.ARROW_CIRCLE_RIGHT, on_click=self.forward_date_func)
        # self.main_bar=ft.Row(controls=[self.back_date,self.title_container,self.forward_date],alignment=ft.MainAxisAlignment.SPACE_EVENLY)
        
        decolate=ft.Icon(name=ft.icons.CALENDAR_MONTH_OUTLINED,size=45,color="#0000cd")
        self.main_bar=ft.Container(content=ft.Row(controls=[decolate,self.title_container,decolate],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                                   bgcolor="Green",
                                   height=100,
                                )
        
        ######################## incorporate ########################     
        

        self.plans=ft.Column(controls=[],expand=True)#ここに，[時間，内容，説明]のlistを入れていく

        #self.plansにlistを作成する関数の実行
        self.calender_list_create()
        
        self.space= ft.Placeholder(color=ft.colors.random_color(),expand=True)#一時的な場所確保

        #このself.contentsをmain.pyで呼び出して使用する．
        self.contents=ft.Column(controls=[self.main_bar,
                                          ft.Container(content=ft.Divider(color="white",height=1.5,thickness=1.5),margin=ft.margin.only(0,0,0,20),),
                                          self.plans
                                        ],expand=True,spacing=0)

    
    def back_date_func(self,e):#TODO関数の作成
        pass
    
    def forward_date_func(self,e):#TODO関数の作成
        pass

    
    def calender_list_create(self):#list_contents_createをforで繰り返してself.contentsのcolumnに入れるリスト作成
        
                
        events=calender.main()
        list_con=[]
        for event in events:
            #eventないときの処理を書く
            if event == None:
                continue
            
            event_time=datetime.datetime.fromisoformat(event["date"]).strftime("%H:%M")
            if event_time=="00:00":
                event_time="All Day"

            bg_color=event["color"]
            
            time=ft.Container(content=ft.Text(event_time,size=35,weight=ft.FontWeight.W_500,color="white"),
                              alignment=ft.alignment.center,
                              width=200,height=50,
                              margin= ft.margin.only(5,10,10,5),padding=0,
                              border_radius=0,
                              )
            plan_con=ft.Container(content=ft.Text(event["summary"],size=35,weight=ft.FontWeight.W_500,bgcolor=bg_color,color="black",expand=True),
                                # alignment=ft.alignment.center,
                                width=530,
                                margin=ft.margin.only(0,0,0,1),padding=ft.padding.symmetric(horizontal=10),
                                border_radius=3,
                                bgcolor=bg_color
                              )        
            description=ft.Container(content=ft.Text(event["desc"],size=28,weight=ft.FontWeight.W_500,color="black",expand=True),
                                # alignment=ft.alignment.center,
                                width=530,
                                margin=0,padding=ft.padding.only(10,0,0,0),
                                border_radius=3,
                                bgcolor=bg_color
                              )
            # print(plan_con.content.value)
            
            if event["desc"]==None:#descriptionに何も記述ない場合はcolumnを作成しない．
                plan_column=plan_con
            else:
                plan_column=ft.Column(controls=[plan_con,description],expand=True,spacing=0)

            list_con=ft.Container(content=ft.Row(controls=[time,plan_column],spacing=10),margin=ft.margin.only(0,10,0,0))

            self.plans.controls.append(list_con)
        return 0
        
        
    def calender_update(self):
        #self.plansを初期化
        self.plans.controls.clear()
        
        # print("initialize")
        events=calender.main()
        # list_con=[]
        for event in events:
            event_time=datetime.datetime.fromisoformat(event["date"]).strftime("%H:%M")
            if event_time=="00:00":
                event_time="All Day"

            bg_color=event["color"]
            
            time=ft.Container(content=ft.Text(event_time,size=35,weight=ft.FontWeight.W_500,color="white"),
                              alignment=ft.alignment.center,
                              width=200,height=50,
                              margin= ft.margin.only(5,10,10,5),padding=0,
                              border_radius=0,
                              )
            plan_con=ft.Container(content=ft.Text(event["summary"],size=35,weight=ft.FontWeight.W_500,bgcolor=bg_color,color="black",expand=True),
                                # alignment=ft.alignment.center,
                                width=530,
                                margin=ft.margin.only(0,0,0,1),padding=ft.padding.symmetric(horizontal=10),
                                border_radius=3,
                                bgcolor=bg_color
                              )
                                 
            description=ft.Container(content=ft.Text(event["desc"],size=28,weight=ft.FontWeight.W_500,color="black",expand=True),
                                # alignment=ft.alignment.center,
                                width=530,
                                margin=0,padding=ft.padding.only(10,0,0,0),
                                border_radius=3,
                                bgcolor=bg_color
                              )
            # print(plan_con.content.value)
            
            if event["desc"]==None:#descriptionに何も記述ない場合はcolumnを作成しない．
                plan_column=plan_con
            else:
                plan_column=ft.Column(controls=[plan_con,description],expand=True,spacing=0)

            list_con=ft.Container(content=ft.Row(controls=[time,plan_column],spacing=10),margin=ft.margin.only(0,10,0,0))
            # print(event["summary"])
            self.plans.controls.append(list_con)
        
        # print("added")
