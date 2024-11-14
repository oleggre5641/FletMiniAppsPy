from time import sleep

import flet as ft

path = ""


def main(page: ft.Page):
    page.title = "ToDoApp"
    page.theme_mode = "light"  # dark
    page.window.width = 450
    page.window.height = 450
    page.window.resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def save(e):
        global path
        f = open(path, "w")
        f.write(text_field.value)
        f.close()
        text_field.value = ""
        save_button.text = "Готово!"
        page.update()
        sleep(1)
        save_button.text = "Сохранить"
        page.update()

    text_field = ft.TextField(label="Текст файла", width=120, multiline=True)
    save_button = ft.FilledButton("Сохранить", on_click=save)

    def pick_result(e: ft.FilePickerResultEvent):
        global path
        if not e.files:
            selected_file.value = "Ничего не выбрано"
        else:
            selected_file.value = ""
            for f in e.files:
                path = f.path

            f = open(path, "r")
            text_field.value = f.read()
            f.close()

        page.update()

    pick_dialog = ft.FilePicker(on_result=pick_result)
    page.overlay.append(pick_dialog)
    selected_file = ft.Text()

    page.add(
        ft.Row([ft.Text("Выбор файла", size=21, weight=500)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(
            [
                ft.ElevatedButton(
                    "Выбрать файл",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: pick_dialog.pick_files(allow_multiple=False)
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row([text_field], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([save_button], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([selected_file], alignment=ft.MainAxisAlignment.CENTER)
    )


ft.app(target=main)

#  Для веб-приложения : view=ft.AppView.WEB_BROWSER
