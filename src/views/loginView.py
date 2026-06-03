import flet as ft

def LoginView(page: ft.Page, auth_controller):

    def mostrar_snackbar(mensaje_texto, color=ft.Colors.GREEN):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje_texto),
            bgcolor=color,
            duration=2000,
        )
        page.snack_bar.open = True
        page.update()

    def login_click(e):
        if not correo.value or not contrasena.value:
            mensaje.value = "Por favor, llene todos los campos"
            mensaje.color = ft.Colors.RED_400
            page.update()
            return
        user, msg = auth_controller.login(correo.value, contrasena.value, page)
        if user:
            try:
                cuentas = page.client_storage.get("perfiles_activos") or []
                if not any(c['id'] == user['id_usuario'] for c in cuentas):
                    cuentas.append({
                        "id": user['id_usuario'],
                        "nombre": user['nombre'],
                        "email": user['email'],
                    })
            except Exception as ex:
                print(f"Error guardando perfil localmente: {ex}")
            page.user_data = user
            mostrar_snackbar("¡Sesión iniciada correctamente!", ft.Colors.GREEN)
            page.go("/dashboard")
        else:
            mensaje.value = msg
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

    correo = ft.TextField(
        label="Correo electrónico",
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
        keyboard_type=ft.KeyboardType.EMAIL,
        **input_style
    )
    contrasena = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        on_submit=login_click,
        **input_style
    )
    mensaje = ft.Text("", color=ft.Colors.RED_400, size=13)

    return ft.View(
        route="/",
        bgcolor=ft.Colors.BLUE_GREY_900,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=440,
                padding=40,
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
                    spacing=18,
                    controls=[
                        ft.Container(
                            width=80, height=80, border_radius=40,
                            bgcolor=ft.Colors.CYAN_900,
                            content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=40, color=ft.Colors.CYAN_300),
                            alignment=ft.alignment.Alignment(0, 0),
                        ),
                        ft.Text("PROSSPERA", size=26, weight="bold", color=ft.Colors.CYAN_100),
                        ft.Text("Inicia sesión en tu cuenta", size=13, color=ft.Colors.WHITE54),
                        ft.Container(height=4),
                        correo,
                        contrasena,
                        mensaje,
                        ft.Container(height=2),
                        ft.ElevatedButton(
                            "ENTRAR AL SISTEMA",
                            width=360, height=50,
                            on_click=login_click,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.CYAN_600,
                                color=ft.Colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=12),
                                elevation=4,
                            ),
                        ),
                        ft.TextButton(
                            "¿Olvidaste tu contraseña?",
                            on_click=lambda _: page.go("/recovery"),
                            style=ft.ButtonStyle(color=ft.Colors.CYAN_300),
                        ),
                        ft.Divider(height=1, color=ft.Colors.BLUE_GREY_700),
                        ft.TextButton(
                            "¿No tienes cuenta? Regístrate aquí",
                            on_click=lambda _: page.go("/register"),
                            style=ft.ButtonStyle(color=ft.Colors.CYAN_200),
                        ),
                    ]
                )
            )
        ]
    )