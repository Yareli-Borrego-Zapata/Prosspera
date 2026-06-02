import flet as ft

from controllers.profileController import ProfileController

profile_controller = ProfileController()

def ProfileView(page: ft.Page):

    usuario = page.user_data

    datos_usuario = profile_controller.obtener_usuario(
        usuario["id_usuario"]
    )


    def cerrar_sesion(e):

        page.user_data = None

        page.go("/")


    def eliminar_cuenta(e):

        eliminado = profile_controller.eliminar_cuenta(
            usuario["id_usuario"]
        )

        if eliminado:

            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    "Cuenta eliminada correctamente"
                ),
                bgcolor=ft.Colors.RED,
            )

            page.snack_bar.open = True

            page.user_data = None

            page.go("/")

        else:

            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    "No se pudo eliminar la cuenta"
                ),
                bgcolor=ft.Colors.RED,
            )

            page.snack_bar.open = True

        page.update()


    return ft.View(

        route="/profile",

        bgcolor=ft.Colors.BLUE_GREY_900,

        controls=[

            ft.AppBar(
                title=ft.Text("Mi Perfil"),
                center_title=True,
                bgcolor=ft.Colors.CYAN_700
            ),

            ft.Container(height=40),

            ft.Column(

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[

                    ft.Icon(
                        ft.Icons.ACCOUNT_CIRCLE,
                        size=120,
                        color=ft.Colors.CYAN_300
                    ),

                    ft.Text(
                        f"{datos_usuario['nombre']} "
                        f"{datos_usuario['apellido']}",
                        size=28,
                        weight="bold",
                        color=ft.Colors.WHITE
                    ),

                    ft.Text(
                        datos_usuario["email"],
                        size=16,
                        color=ft.Colors.WHITE70
                    ),

                    ft.Container(height=40),

                    ft.ElevatedButton(

                        "Cerrar sesión",

                        width=260,

                        bgcolor=ft.Colors.ORANGE,

                        color=ft.Colors.WHITE,

                        on_click=cerrar_sesion
                    ),

                    ft.ElevatedButton(

                        "Eliminar cuenta",

                        width=260,

                        bgcolor=ft.Colors.RED,

                        color=ft.Colors.WHITE,

                        on_click=eliminar_cuenta
                    ),

                    ft.Container(height=20),

                    ft.TextButton(
                        "Volver al inicio",
                        on_click=lambda e: page.go("/dashboard")
                    )
                ]
            )
        ]
    )