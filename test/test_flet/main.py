# #!/usr/bin/env python3

###########################################
#チュートリアル　todo app
###########################################
import flet as ft
class TodoApp(ft.Column):#ft.Coulmnが親クラス
    def __init__(self):
        super().__init__()#ft.Column（親クラス）のコンストラクタを継承
        self.new_task=ft.TextField(hint_text="what",expand=True)
        self.tasks=ft.Column()
        # self.tasks_view=ft.Column()
        self.width=600
        self.controls=[
            ft.Row(controls=[self.new_task , ft.FloatingActionButton(icon=ft.icons.ADD,on_click=self.add_clicked),],),
            self.tasks,
        ]
        
    def add_clicked(self,e):#引数eはon_click時に自動的に渡されるイベント発生時の情報を格納したobject
        task=Task(self.new_task.value,self.task_delete)#taskとして新しいtaksのインスタンスを作成
        self.tasks.controls.append(task)
        self.new_task.value=""
        self.update()
        
        
    def task_delete(self,task):
        self.tasks.controls.remove(task)
        self.update()
    
def  main(page:ft.Page):
    page.title="to do page"
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.update()
    
    todo=TodoApp()
    page.add(todo)
    
    
    
# Task class
class Task(ft.Column):
    def __init__(self,task_name,task_delete):
        super().__init__()
        self.task_name=task_name
        self.task_delete=task_delete
        self.display_task=ft.Checkbox(value=False,label=self.task_name)
        self.edit_name=ft.TextField(expand=True)
        
        self.display_view=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(icon=ft.icons.CREATE_OUTLINED,tooltip="Edit To-Do",on_click=self.edit_clicked),
                        ft.IconButton(ft.icons.DELETE_OUTLINE,tooltip="Delete To-Do",on_click=self.delete_clicked),
                    ],
                ),
            ],
        )
        
        self.edit_view=ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(icon=ft.icons.DONE_OUTLINE_OUTLINED,icon_color=ft.colors.GREEN,tooltip="Update To-Do",on_click=self.save_clicked,),
            ],
        )
        
        self.controls=[self.display_view,self.edit_view]
        
    
    def edit_clicked(self,e):
        self.edit_name.value=self.display_task.label
        self.display_view.visible=False
        self.edit_view.visible=True
        self.update()
        
    def save_clicked(self,e):
        self.display_task.label=self.edit_name.value
        self.display_view.visible=True
        self.edit_view.visible=False
        self.update()
        
    def delete_clicked(self,e):
        self.task_delete(self)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

ft.app(main)