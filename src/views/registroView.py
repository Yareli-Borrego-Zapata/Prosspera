import flet as ft
import re
from models.schemasModel import UsuarioSchema

def RegisterView(page: ft.Page, auth_controller):

    def mostrar_snackbar(mensaje_texto, color=ft.Colors.GREEN):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje_texto),
            bgcolor=color,
            duration=2000,
        )
        page.snack_bar.open = True
        page.update()

    def registrar_click(e):
        if not nombre.value or not apellido.value or not email.value or not password.value or not confirm_password.value:
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = ft.Colors.RED_400
            page.update()
            return
        if password.value != confirm_password.value:
            mensaje.value = "Las contraseñas no coinciden"
            mensaje.color = ft.Colors.RED_400
            page.update()
            return
        if len(password.value) < 8:
            mensaje.value = "La contraseña debe tener al menos 8 caracteres"
            mensaje.color = ft.Colors.RED_400
            page.update()
            return
        if not re.search(r'[A-Z]', password.value):
            mensaje.value = "La contraseña debe tener al menos una mayúscula"
            mensaje.color = ft.Colors.RED_400
            page.update()
            return
        if not re.search(r'[a-z]', password.value):
            mensaje.value = "La contraseña debe tener al menos una minúscula"
            mensaje.color = ft.Colors.RED_400
            page.update()
            return
        if not re.search(r'[0-9]', password.value):
            mensaje.value = "La contraseña debe tener al menos un número"
            mensaje.color = ft.Colors.RED_400
            page.update()
            return
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email.value):
            mensaje.value = "Correo electrónico inválido"
            mensaje.color = ft.Colors.RED_400
            page.update()
            return
        try:
            usuario_data = UsuarioSchema(
                nombre=nombre.value, apellido=apellido.value,
                email=email.value, password=password.value
            )
        except Exception as ex:
            mensaje.value = str(ex.errors()[0]['msg']).replace('Value error, ', '')
            mensaje.color = ft.Colors.RED_400
            page.update()
            return
        exito, msg = auth_controller.registrar(usuario_data)
        if exito:
            mostrar_snackbar("¡Registro exitoso! Ahora inicia sesión", ft.Colors.GREEN)
            page.go("/")
        else:
            mensaje.value = msg or "Error al registrar usuario"
            mensaje.color = ft.Colors.RED_400
            page.update()

    input_style = {
        "width": 360,
        "border_radius": 12,
        "border_color": ft.Colors.CYAN_700,
        "focused_border_color": ft.Colors.CYAN_400,
        "color": ft.Colors.WHITE,
        "label_style": ft.TextStyle(color=ft.Colors.CYAN_200),
        "bgcolor": ft.Colors.BLUE_GREY_800,
        "cursor_color": ft.Colors.CYAN_400,
    }

    nombre = ft.TextField(label="Nombre(s)", prefix_icon=ft.Icons.PERSON_OUTLINE, **input_style)
    apellido = ft.TextField(label="Apellidos", prefix_icon=ft.Icons.PERSON_PIN_OUTLINED, **input_style)
    email = ft.TextField(label="Correo electrónico", prefix_icon=ft.Icons.EMAIL_OUTLINED, keyboard_type=ft.KeyboardType.EMAIL, **input_style)
    password = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        hint_text="Mín. 8 chars, mayúscula, minúscula y número",
        hint_style=ft.TextStyle(color=ft.Colors.WHITE38, size=11),
        **input_style
    )
    confirm_password = ft.TextField(
        label="Confirmar contraseña",
        prefix_icon=ft.Icons.LOCK_RESET_OUTLINED,
        password=True,
        can_reveal_password=True,
        **input_style
    )
    mensaje = ft.Text("", color=ft.Colors.RED_400, size=13)

    return ft.View(
        route="/register",
        bgcolor=ft.Colors.BLUE_GREY_900,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color=ft.Colors.CYAN_400,
                tooltip="Volver al inicio de sesión",
                on_click=lambda _: page.go("/")
            ),
            bgcolor=ft.Colors.BLUE_GREY_900,
            elevation=0,
        ),
        controls=[
            ft.Container(
                width=440,
                padding=35,
                border_radius=28,
                border=ft.Border(
                    top=ft.BorderSide(1.5, ft.Colors.CYAN_800),
                    bottom=ft.BorderSide(1.5, ft.Colors.CYAN_800),
                    left=ft.BorderSide(1.5, ft.Colors.CYAN_800),
                    right=ft.BorderSide(1.5, ft.Colors.CYAN_800),
                ),
                shadow=ft.BoxShadow(blur_radius=40, color=ft.Colors.BLACK54, offset=ft.Offset(0, 12)),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=14,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    controls=[
                        ft.Container(
                            width=70, height=70, border_radius=35,
                            bgcolor=ft.Colors.CYAN_900,
                            content=ft.Icon(ft.Icons.PERSON_ADD_ALT_1_ROUNDED, size=34, color=ft.Colors.CYAN_300),
                            alignment=ft.alignment.Alignment(0, 0),
                        ),
                        ft.Text("CREAR CUENTA", size=24, weight="bold", color=ft.Colors.CYAN_100),
                        ft.Text("Completa los datos para continuar", size=13, color=ft.Colors.WHITE54),
                        ft.Container(height=2),
                        nombre,
                        apellido,
                        email,
                        password,
                        confirm_password,
                        mensaje,
                        ft.ElevatedButton(
                            "REGISTRARME",
                            width=360, height=50,
                            on_click=registrar_click,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.CYAN_600,
                                color=ft.Colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=12),
                                elevation=4,
                            ),
                        ),
                        ft.Divider(height=1, color=ft.Colors.BLUE_GREY_700),
                        ft.TextButton(
                            "¿Ya tienes cuenta? Inicia sesión",
                            on_click=lambda _: page.go("/"),
                            style=ft.ButtonStyle(color=ft.Colors.CYAN_200),
                        ),
                    ]
                )
            )
        ]
    )