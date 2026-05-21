import flet as ft

def RecoveryView(page: ft.Page, auth_controller):

    estado = {"codigo": None}

    def mostrar_snackbar(mensaje_texto, color=ft.Colors.GREEN):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje_texto),
            bgcolor=color,
            duration=3000,
        )
        page.snack_bar.open = True
        page.update()


    def enviar_codigo_click(e):
        if not correo.value:
            mensaje_error.value = "Por favor, introduce tu correo electrónico"
            mensaje_error.color = ft.Colors.RED_400
            page.update()
            return
        
        
        codigo = auth_controller.enviar_correo_recuperacion(correo.value)
        
        if codigo:
            estado["codigo"] = str(codigo)  
            mostrar_snackbar("Código enviado. Revisa tu bandeja de entrada.", ft.Colors.GREEN)
            
        
            paso_correo.visible = False
            paso_restablecer.visible = True
            mensaje_error.value = ""
            page.update()
        else:
            mensaje_error.value = "El correo no está registrado o falló el servidor."
            mensaje_error.color = ft.Colors.RED_400
            page.update()

    
    def restablecer_password_click(e):
        if not token_input.value or not nueva_pass.value or not confirmar_pass.value:
            mensaje_error.value = "Por favor, completa todos los campos"
            mensaje_error.color = ft.Colors.RED_400
            page.update()
            return
        
        if token_input.value.strip() != estado["codigo"]:
            mensaje_error.value = "El código ingresado es incorrecto"
            mensaje_error.color = ft.Colors.RED_400
            page.update()
            return
            
        if nueva_pass.value != confirmar_pass.value:
            mensaje_error.value = "Las contraseñas no coinciden"
            mensaje_error.color = ft.Colors.RED_400
            page.update()
            return

        if len(nueva_pass.value) < 6:
            mensaje_error.value = "La contraseña debe tener al menos 6 caracteres"
            mensaje_error.color = ft.Colors.RED_400
            page.update()
            return
            
        exito, msg = auth_controller.actualizar_password(correo.value, nueva_pass.value)
        
        if exito:
            mostrar_snackbar("¡Contraseña actualizada con éxito!", ft.Colors.GREEN)
            page.go("/")  
        else:
            mensaje_error.value = msg or "Error al actualizar"
            mensaje_error.color = ft.Colors.RED_400
            page.update()



    input_style = {
        "width": 380,
        "border_radius": 12,
        "border_color": ft.Colors.CYAN_400,
        "color": ft.Colors.WHITE,
        "label_style": ft.TextStyle(color=ft.Colors.CYAN_200),
        "bgcolor": ft.Colors.BLUE_GREY_800,
    }
    
    mensaje_error = ft.Text("", color=ft.Colors.RED_400, weight="w500")


    correo = ft.TextField(label="Correo electrónico", prefix_icon=ft.Icons.EMAIL_OUTLINED, **input_style)

    paso_correo = ft.Column(
        [
            ft.Text("RECUPERAR CUENTA", size=26, weight="bold", color=ft.Colors.CYAN_100),
            ft.Text("Introduce tu correo para validar tu identidad", size=14, color=ft.Colors.WHITE70),
            ft.Container(height=10),
            correo,
            ft.ElevatedButton(
                "ENVIAR CÓDIGO",
                width=380,
                height=50,
                on_click=enviar_codigo_click,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.CYAN_600,
                    color=ft.Colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=12),
                ),
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12
    )


    token_input = ft.TextField(label="Código de verificación (6 dígitos)", prefix_icon=ft.Icons.PIN, **input_style)
    nueva_pass = ft.TextField(label="Nueva Contraseña", prefix_icon=ft.Icons.LOCK_OUTLINE, password=True, can_reveal_password=True, **input_style)
    confirmar_pass = ft.TextField(label="Confirmar Nueva Contraseña", prefix_icon=ft.Icons.LOCK_RESET_OUTLINED, password=True, can_reveal_password=True, **input_style)

    paso_restablecer = ft.Column(
        [
            ft.Text("RESETEAR CLAVE", size=26, weight="bold", color=ft.Colors.CYAN_100),
            ft.Text("Introduce el código enviado y tu nueva clave", size=14, color=ft.Colors.WHITE70),
            ft.Container(height=10),
            token_input,
            nueva_pass,
            confirmar_pass,
            ft.ElevatedButton(
                "CAMBIAR CONTRASEÑA",
                width=380,
                height=50,
                on_click=restablecer_password_click,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.CYAN_600,
                    color=ft.Colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=12),
                ),
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        visible=False
    )

    btn_volver = ft.TextButton(
        "Regresar al Inicio de Sesión",
        on_click=lambda _: page.go("/"),
        style=ft.ButtonStyle(color=ft.Colors.CYAN_200)
    )

    return ft.View(
        route="/recovery",
        bgcolor=ft.Colors.BLUE_GREY_900,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.LOCK_RESET_ROUNDED, size=90, color=ft.Colors.CYAN_400),
                        paso_correo,
                        paso_restablecer,
                        mensaje_error,
                        btn_volver
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
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
                ),
                width=450
            )
        ]
    )