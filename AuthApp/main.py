import flet as ft
import sqlite3


def main(page: ft.Page):
    page.title = "ToDoApp"
    page.theme_mode = "light"  # dark
    page.window.width = 600
    page.window.height = 400
    page.window.resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def register(e):
        db = sqlite3.connect("my_database")

        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            login TEXT,
            pass TEXT
        )""")

        cur.execute(f"INSERT INTO users VALUES(NULL, '{user_login.value}','{user_pass.value}')")

        db.commit()
        db.close()

        user_login.value = ""
        user_pass.value = ""
        button_reg.text = "Успешно добавлено"
        page.update()

    def validate(e):
        if all([user_login.value, user_pass.value]):
            button_reg.disabled = False
            button_auth.disabled = False
        else:
            button_reg.disabled = True
            button_auth.disabled = True
        page.update()

    def auth(e):
        db = sqlite3.connect("my_database")
        cur = db.cursor()

        cur.execute(f"SELECT * FROM users WHERE login = '{user_login.value}' AND pass ='{user_pass.value}'")

        if cur.fetchone() != None:
            user_login.value = ""
            user_pass.value = ""
            button_auth.text = "Успешно авторизованно"

            if len(page.navigation_bar.destinations) == 2:
                page.navigation_bar.destinations.append(ft.NavigationDestination(
                    icon=ft.icons.BOOK,
                    label="Кабинет",
                    selected_icon=ft.icons.BOOKMARK
                ))

            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Вы неправильно ввели данные, попробуйте ещё раз"))
            page.snack_bar.open = True
            page.update()

    user_login = ft.TextField(label="Логин", width=200, on_change=validate)
    user_pass = ft.TextField(label="Пароль", password=True ,width=200, on_change=validate)
    button_reg = ft.ElevatedButton(text="Добавить", width=200, on_click=register, disabled=True)
    button_auth = ft.ElevatedButton(text="Авторизовать", width=200, on_click=auth, disabled=True)

    # User Cabinet
    users_list = ft.ListView(spacing=10, padding=20)

    panel_register = ft.Row(
    [
                ft.Column(
                    [
                        ft.Text("Регистрация"),
                        user_login,
                        user_pass,
                        button_reg,
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    panel_auth = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Авторизация"),
                    user_login,
                    user_pass,
                    button_auth,
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    panel_cabinet = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Личный кабинет"),
                    users_list
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    def navigate(e):
        index = page.navigation_bar.selected_index
        page.clean()

        if index == 0:
            page.add(panel_register)
        elif index == 1:
            page.add(panel_auth)
        elif index == 2:
            users_list.controls.clear()

            db = sqlite3.connect("my_database")
            cur = db.cursor()
            cur.execute("SELECT * FROM users")
            res = cur.fetchall()
            if res != None:
                for i in res:
                    print(i)
                    users_list.controls.append(ft.Row([
                        ft.Text(i[1]),
                        ft.Icon(ft.icons.ADOBE_ROUNDED)
                    ]))
            db.commit()
            db.close()
            page.add(panel_cabinet)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.VERIFIED_OUTLINED, label="Регистрация"),
            ft.NavigationDestination(icon=ft.icons.VERIFIED_SHARP, label="Авторизация"),
        ], on_change=navigate
    )

    page.add(panel_auth)


ft.app(target=main)

#  Для веб-приложения : view=ft.AppView.WEB_BROWSER
