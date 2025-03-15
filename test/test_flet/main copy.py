# #!/usr/bin/env python3

###########################################
#チュートリアル　todo app
###########################################
import flet as ft
class TodoApp(ft.Column):#ft.Coulmnが親クラス
    def __init__(self):
        super().__init__()#ft.Column（親クラス）のコンストラクタを継承
        self.new_task=ft.TextField(hint_text="what",expand=True)
        self.tasks_view=ft.Column()
        self.width=600
        self.controls=[
            ft.Row(controls=[self.new_task,
                             ft.FloatingActionButton(icon=ft.icons.ADD,on_click=self.add_clicked),],),
            self.tasks_view,
        ]
        
    def add_clicked(self,e):#引数eはon_click時に自動的に渡されるイベント発生時の情報を格納したobject
        self.tasks_view.controls.append(ft.Checkbox(label=self.new_task.value))
        self.new_task.value=""
        self.update()
    
def  main(page:ft.Page):
    page.title="to do page"
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.update()
    
    todo=TodoApp()
    page.add(todo)
    
    
    
# Task class
class Task(ft.Column):
    def __init__
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

ft.app(main)