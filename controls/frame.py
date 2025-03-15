import flet as ft

class frame_class(ft.Row):
    def __init__(self,frame_title):
        super().__init__()
        
        self.title=ft.Text(frame_title, theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM,weight=ft.FontWeight.W_500,)#TODOディスプレイのサイズに合わせて文字の大きさも変わるようにしたいね．
        self.title_container=ft.Container(content=self.title,alignment=ft.alignment.center)#containerを使ってTitleを中央配置
        
        
        
        self.col=ft.Column(controls=[self.title_container,
                                     ft.Divider(color="white",height=1.5,thickness=1.5),
                                    ],expand=True)#expandで横画面の大きさに合わせる,height,thicknessでdividerの幅設定．

