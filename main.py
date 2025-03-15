# -*-coding: utf-8 -*-
#!/usr/bin/env python
from controls import calender_con
from controls import tasks_con
import flet as ft
import time
    
import logging    
logging.basicConfig(
    filename="log.txt",
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s-%(message)s",
    encoding="utf-8")
    
logging.info("script was run")

def switch_disabled():
    tasks_num=len(tasks.remain.controls)
    for i in range(tasks_num):
        tasks.remain.controls[i].content.controls[-1].disabled=True
    tasks_num=len(tasks.completed.controls)
    for i in range(tasks_num):
        tasks.remain.controls[i].content.controls[-1].disabled=True

def switch_abled():
    tasks_num=len(tasks.remain.controls)
    for i in range(tasks_num):
        tasks.remain.controls[i].content.controls[-1].disabled=False
    tasks_num=len(tasks.completed.controls)
    for i in range(tasks_num):
        tasks.remain.controls[i].content.controls[-1].disabled=False


def main(page: ft.Page):
    #iPad用のwindowサイズにしておく．
    #page.window.width=1024
    #page.window.height=768
    page.window.width=1600
    page.window.height=900
    page.fonts={
            "Go_bd":"/home/kayu/Desktop/plan/assets/LINESeedJP_TTF_Bd.ttf"
    }
    page.bgcolor="black"
    page.color="white"
    page.theme=ft.Theme(font_family="Go_bd")
    page.horizontal_alignment=ft.CrossAxisAlignment.STRETCH
    page.title="Plan Bulletin"
    
    global calender, tasks
    calender=calender_con.calender_contents()
    tasks=tasks_con.tasks_contents(page)    
    logging.info("got info")
    
    app=ft.Row(controls=[
                        calender.contents,#tasks開発のために一度実行しない．
                        ft.VerticalDivider(color="white",width=1.5,thickness=1.5),#CalenderとTasksの区切り線
                        tasks.contents],
                expand=True,spacing=0)#expandで縦画面サイズに合わせる,spacing=0でdividerの区切り消す．
    
    logging.info("creating page")
    page.add(app)

    timer=0
    while 1:
        logging.info("repeating")
        calender.calender_update()#これを実行するとカレンダーの内容がupdateされる．
        
        if timer>300:
            #tasksのスイッチをdisabledにする．
            switch_disabled()
            page.update()
            #ここからがTaskの方を自動更新するプログラム．
            tasks.tasks_list_create()#これを実行するとtasksがupdateされる．
            #tasksのスイッチをabledにする．
            switch_abled()
            timer=0
        page.update()
        time.sleep(1)
        timer+=1



logging.info("before ft.app")
ft.app(main)
logging.info("after ft.app")
