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
        if not nombre.value or not email.value or not password.value or not confirm_password.value:
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = ft.Colors.RED_400
            page.update()
            return
        
        if password.value != confirm_password.value:
            mensaje.value = "Las contraseñas no coinciden"
            mensaje.color = ft.Colors.RED_400
            page.update()
            return
        
        if len(password.value) < 6:
            mensaje.value = "La contraseña debe tener al menos 6 caracteres"
            mensaje.color = ft.Colors.RED_400
            page.update()
            return
        
        if not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            email.value
        ):
            mensaje.value = "Correo electrónico inválido"
            mensaje.color = ft.Colors.RED_400
            page.update()
            return
        
        usuario_data = UsuarioSchema(
            nombre=nombre.value,
            apellido=apellido.value,
            email=email.value,
            password=password.value
        )
        
        exito, msg = auth_controller.registrar(usuario_data)
        
        if exito:
            mostrar_snackbar("¡Registro exitoso! Ahora inicia sesión", ft.Colors.GREEN)
            nombre.value = ""
            apellido.value = ""
            email.value = ""
            password.value = ""
            confirm_password.value = ""
            mensaje.value = ""
            page.update()
            page.go("/")
        else:
            mensaje.value = msg or "Error al registrar usuario"
            mensaje.color = ft.Colors.RED_400
            page.update()
    
    def ir_login(e):
        page.go("/")

    #diseño
    
    input_style = {
        "width": 380,
        "border_radius": 12,
        "border_color": ft.Colors.CYAN_400,
        "color": ft.Colors.WHITE,
        "label_style": ft.TextStyle(color=ft.Colors.CYAN_200),
        "bgcolor": ft.Colors.BLUE_GREY_800,
    }

    nombre = ft.TextField(label="Nombre(s)", prefix_icon=ft.Icons.PERSON_OUTLINE, **input_style)
    apellido = ft.TextField(label="Apellidos", prefix_icon=ft.Icons.PERSON_PIN_OUTLINED, **input_style)
    email = ft.TextField(label="Correo electrónico", prefix_icon=ft.Icons.EMAIL_OUTLINED, keyboard_type=ft.KeyboardType.EMAIL, **input_style)
    password = ft.TextField(label="Contraseña", prefix_icon=ft.Icons.LOCK_OUTLINE, password=True, can_reveal_password=True, **input_style)
    confirm_password = ft.TextField(label="Confirmar contraseña", prefix_icon=ft.Icons.LOCK_RESET_OUTLINED, password=True, can_reveal_password=True, **input_style)
    
    mensaje = ft.Text("", color=ft.Colors.RED_400, weight="w500")
    
    btn_registrar = ft.ElevatedButton(
        "CREAR CUENTA",
        width=380,
        height=50,
        on_click=registrar_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.CYAN_600,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )
    
    btn_login = ft.TextButton(
        "¿Ya tienes cuenta? Inicia sesión",
        on_click=ir_login,
        style=ft.ButtonStyle(color=ft.Colors.CYAN_200)
    )
    
    return ft.View(
        route="/register",
        bgcolor=ft.Colors.BLUE_GREY_900,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            title=ft.Text("Registro de Usuario"),
            bgcolor=ft.Colors.TRANSPARENT,
            color=ft.Colors.WHITE,
            leading=ft.IconButton(
                ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color=ft.Colors.CYAN_400,
                on_click=lambda _: page.go("/")
            )
        ),
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "NUEVO PERFIL",
                            size=28,
                            weight="bold",
                            color=ft.Colors.CYAN_100,
                            
                        ),
                        ft.Text(
                            "Completa los datos para continuar",
                            size=14,
                            color=ft.Colors.WHITE70
                        ),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        nombre,
                        apellido,
                        email,
                        password,
                        confirm_password,
                        mensaje,
                        ft.Container(height=10),
                        btn_registrar,
                        btn_login
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                    scroll=ft.ScrollMode.ADAPTIVE
                ),
                padding=40,
                border_radius=25,
                #tambien le d un borde y sombra para que se vea como una tarjeta
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
#hola esmeraldas, este es el nuevo diseño de registro, con validaciones y todo avers