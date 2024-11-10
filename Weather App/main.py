import flet as ft
import requests


def main(page: ft.Page):
    page.title = "ToDoApp"
    page.theme_mode = "light"  # dark
    page.window.width = 600
    page.window.height = 400
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    user_data = ft.TextField(label="Введите город", width=400)
    weather_data = ft.Text("")

    def get_info(e):
        if len(user_data.value) < 2:
            return

        # API = "your API"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={user_data.value}&appid={"your APA"}&units=metric"
        res = requests.get(url).json()
        temp = res["main"]["temp"]
        weather_data.value = f"Погода: {str(temp)}"
        page.update()

    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.SUNNY, on_click=change_theme),
                ft.Text("Погода"),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row([user_data], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([weather_data], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([ft.ElevatedButton(text="Получить", on_click=get_info)], alignment=ft.MainAxisAlignment.CENTER)
    )


ft.app(target=main)

#  Для веб-приложения : view=ft.AppView.WEB_BROWSER
