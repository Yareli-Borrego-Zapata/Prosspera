import flet as ft

def LoginView(page: ft.Page, auth_controller):

    def rellenar_campos(datos):
        correo.value = datos.get('email', '')
        contraseña.focus()
        page.update()

    def mostrar_snackbar(mensaje_texto, color=ft.Colors.GREEN):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje_texto),
            bgcolor=color,
            duration=2000,
        )
        page.snack_bar.open = True
        page.update()
        

    def login_click(e):
        if not correo.value or not contraseña.value:
            mensaje.value = "Por favor, llene todos los campos"
            mensaje.color = ft.Colors.RED_400
            page.update()
            return
        
        user, msg = auth_controller.login(correo.value, contraseña.value, page)
        
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

    correo = ft.TextField(
        label="Correo electrónico",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        width=380,
        border_radius=12,
        border_color=ft.Colors.CYAN_400,
        color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.CYAN_200),
        bgcolor=ft.Colors.BLUE_GREY_800,
    )

    contraseña = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        width=380,
        border_radius=12,
        border_color=ft.Colors.CYAN_400,
        color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.CYAN_200),
        bgcolor=ft.Colors.BLUE_GREY_800,
        on_submit=login_click
    )
    
    mensaje = ft.Text("", color=ft.Colors.RED_400)

    btn_olvido = ft.TextButton(
        "¿Olvidaste tu contraseña?",
        on_click=lambda _: page.go("/recovery"),
        style=ft.ButtonStyle(color=ft.Colors.CYAN_200)
    )

    iniciar_sesion = ft.ElevatedButton(
        "ENTRAR AL SISTEMA",
        width=380,
        height=50,
        on_click=login_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.CYAN_600,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )
    
    btn_registro = ft.TextButton(
        "¿No tienes cuenta? Regístrate aquí",
        on_click=lambda _: page.go("/register"),
        style=ft.ButtonStyle(color=ft.Colors.CYAN_200)
    )

    return ft.View(
        route="/",
        bgcolor=ft.Colors.BLUE_GREY_900,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.ACCOUNT_CIRCLE_SHARP, size=90, color=ft.Colors.CYAN_400),
                        ft.Text("Iniciar Sesión", size=28, weight="bold", color=ft.Colors.CYAN_100),
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        correo,
                        contraseña,
                        mensaje,
                        iniciar_sesion,
                        ft.Column(
                            [
                                btn_olvido,
                                btn_registro
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                padding=40,
                border_radius=25,
                border=ft.Border(
                    top=ft.BorderSide(2, ft.Colors.CYAN_800),
                    bottom=ft.BorderSide(2, ft.Colors.CYAN_800),
                    left=ft.BorderSide(2, ft.Colors.CYAN_800),
                    right=ft.BorderSide(2, ft.Colors.CYAN_800)
                ),
                shadow=ft.BoxShadow(
                    blur_radius=30, 
                    color=ft.Colors.BLACK45,
                    offset=ft.Offset(0, 10)
                )
            )
        ]
    )