import flet as ft
from controllers.profileController import ProfileController

profile_controller = ProfileController()

def ProfileView(page: ft.Page):

    usuario = page.user_data
    datos_usuario = profile_controller.obtener_usuario(usuario["id_usuario"])

    def cerrar_sesion(e):
        page.user_data = None
        page.go("/")

    def eliminar_cuenta(e):
        def confirmar(ev):
            dialog.open = False
            page.update()
            eliminado = profile_controller.eliminar_cuenta(usuario["id_usuario"])
            if eliminado:
                page.snack_bar = ft.SnackBar(ft.Text("Cuenta eliminada correctamente"), bgcolor=ft.Colors.RED_700)
                page.snack_bar.open = True
                page.user_data = None
                page.go("/")
            else:
                page.snack_bar = ft.SnackBar(ft.Text("No se pudo eliminar la cuenta"), bgcolor=ft.Colors.RED_700)
                page.snack_bar.open = True
                page.update()

        def cancelar(ev):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("¿Eliminar cuenta?", color=ft.Colors.WHITE, weight="bold"),
            content=ft.Text("Esta acción es irreversible. Se borrarán todos tus datos.", color=ft.Colors.WHITE70),
            bgcolor=ft.Colors.BLUE_GREY_900,
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar, style=ft.ButtonStyle(color=ft.Colors.CYAN_300)),
                ft.ElevatedButton("Eliminar", on_click=confirmar,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE)),
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    inicial = datos_usuario['nombre'][0].upper() if datos_usuario else "?"

    return ft.View(
        route="/profile",
        bgcolor=ft.Colors.BLUE_GREY_900,
        appbar=ft.AppBar(
            title=ft.Text("Mi Perfil", size=20, weight="bold", color=ft.Colors.WHITE),
            center_title=True,
            bgcolor=ft.Colors.BLUE_GREY_900,
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color=ft.Colors.CYAN_400,
                on_click=lambda _: page.go("/dashboard")
            ),
        ),
        controls=[
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Container(height=20),
                        ft.Container(
                            width=100, height=100, border_radius=50,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.Alignment(-1, -1),
                                end=ft.alignment.Alignment(1, 1),
                                colors=[ft.Colors.CYAN_700, ft.Colors.BLUE_900]
                            ),
                            content=ft.Text(inicial, size=42, weight="bold", color=ft.Colors.WHITE),
                            alignment=ft.alignment.Alignment(0, 0),
                        ),
                        ft.Text(
                            f"{datos_usuario['nombre']} {datos_usuario['apellido']}",
                            size=26, weight="bold", color=ft.Colors.WHITE
                        ),
                        ft.Text(datos_usuario["email"], size=14, color=ft.Colors.WHITE54),
                        ft.Container(height=10),
                        ft.Container(
                            width=380, padding=25, border_radius=20,
                            bgcolor=ft.Colors.BLUE_GREY_800,
                            border=ft.Border(
                                top=ft.BorderSide(1, ft.Colors.CYAN_800),
                                bottom=ft.BorderSide(1, ft.Colors.CYAN_800),
                                left=ft.BorderSide(1, ft.Colors.CYAN_800),
                                right=ft.BorderSide(1, ft.Colors.CYAN_800),
                            ),
                            content=ft.Column(spacing=16, controls=[
                                ft.Row(controls=[
                                    ft.Icon(ft.Icons.PERSON_OUTLINE, color=ft.Colors.CYAN_400, size=20),
                                    ft.Text("Nombre", color=ft.Colors.WHITE54, size=13),
                                    ft.Text(datos_usuario['nombre'], color=ft.Colors.WHITE, weight="bold", size=14),
                                ], spacing=12),
                                ft.Divider(height=1, color=ft.Colors.BLUE_GREY_700),
                                ft.Row(controls=[
                                    ft.Icon(ft.Icons.BADGE_OUTLINED, color=ft.Colors.CYAN_400, size=20),
                                    ft.Text("Apellido", color=ft.Colors.WHITE54, size=13),
                                    ft.Text(datos_usuario['apellido'], color=ft.Colors.WHITE, weight="bold", size=14),
                                ], spacing=12),
                                ft.Divider(height=1, color=ft.Colors.BLUE_GREY_700),
                                ft.Row(controls=[
                                    ft.Icon(ft.Icons.EMAIL_OUTLINED, color=ft.Colors.CYAN_400, size=20),
                                    ft.Text("Correo", color=ft.Colors.WHITE54, size=13),
                                    ft.Text(datos_usuario['email'], color=ft.Colors.WHITE, weight="bold", size=13),
                                ], spacing=12),
                            ])
                        ),
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            "Cerrar sesión",
                            width=380, height=50,
                            icon=ft.Icons.LOGOUT_ROUNDED,
                            on_click=cerrar_sesion,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.BLUE_GREY_700,
                                color=ft.Colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=12),
                            ),
                        ),
                        ft.ElevatedButton(
                            "Eliminar cuenta",
                            width=380, height=50,
                            icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                            on_click=eliminar_cuenta,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.RED_900,
                                color=ft.Colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=12),
                            ),
                        ),
                    ]
                )
            )
        ]
    )