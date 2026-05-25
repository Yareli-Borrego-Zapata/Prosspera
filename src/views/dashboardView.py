import flet as ft


def DashboardView(page: ft.Page):

    usuario = getattr(page, "user_data", {})

    nombre = usuario.get("nombre", "Usuario")

    return ft.View(
        route="/dashboard",
        bgcolor=ft.Colors.BLUE_GREY_900,

        appbar=ft.AppBar(
            title=ft.Text(
                "PROSSPERA",
                color=ft.Colors.WHITE
            ),
            bgcolor=ft.Colors.CYAN_700,
            center_title=True,
        ),

        controls=[

            ft.Container(
                expand=True,

                content=ft.Column(
                    [

                        ft.Container(height=40),

                        ft.Icon(
                            ft.Icons.ACCOUNT_BALANCE_WALLET,
                            size=100,
                            color=ft.Colors.CYAN_400
                        ),

                        ft.Text(
                            f"Bienvenid@, {nombre}",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),

                        ft.Text(
                            "Has iniciado sesión correctamente",
                            size=16,
                            color=ft.Colors.WHITE70
                        ),

                        ft.Container(height=30),

                        ft.Row(
                            [
                                ft.Container(
                                    width=160,
                                    height=120,
                                    bgcolor=ft.Colors.CYAN_700,
                                    border_radius=20,

                                    content=ft.Column(
                                        [
                                            ft.Icon(
                                                ft.Icons.ATTACH_MONEY,
                                                color=ft.Colors.WHITE,
                                                size=40
                                            ),

                                            ft.Text(
                                                "Ingresos",
                                                color=ft.Colors.WHITE,
                                                size=18,
                                                weight=ft.FontWeight.BOLD
                                            ),

                                            ft.Text(
                                                "$0.00",
                                                color=ft.Colors.WHITE,
                                                size=22
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                    )
                                ),

                                ft.Container(
                                    width=160,
                                    height=120,
                                    bgcolor=ft.Colors.RED_400,
                                    border_radius=20,

                                    content=ft.Column(
                                        [
                                            ft.Icon(
                                                ft.Icons.MONEY_OFF,
                                                color=ft.Colors.WHITE,
                                                size=40
                                            ),

                                            ft.Text(
                                                "Gastos",
                                                color=ft.Colors.WHITE,
                                                size=18,
                                                weight=ft.FontWeight.BOLD
                                            ),

                                            ft.Text(
                                                "$0.00",
                                                color=ft.Colors.WHITE,
                                                size=22
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                    )
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),

                        ft.Container(height=40),

                        ft.ElevatedButton(
                            "Cerrar sesión",

                            on_click=lambda _: page.go("/"),

                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.RED_400,
                                color=ft.Colors.WHITE,
                                padding=20,
                                shape=ft.RoundedRectangleBorder(radius=12)
                            )
                        )

                    ],

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO
                )
            )
        ]
    )