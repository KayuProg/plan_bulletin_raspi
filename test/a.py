import flet as ft
import time
def main(page: ft.Page):
    def disable_switch(e):
        switch.disabled = True  # スイッチを無効化
        page.update()
        time.sleep(1)
        switch.disabled= False
        page.update()

    switch = ft.Switch(label="Toggle Me")  # 初期状態では有効
    button = ft.ElevatedButton("Disable Switch", on_click=disable_switch)

    page.add(switch, button)

ft.app(target=main)
