import flet as ft

def DashboardView(page: ft.Page):

    usuario = page.user_data

    def ir_perfil(e):
        page.go("/profile")

    def cerrar_sesion(e):

        page.user_data = None

        page.go("/")


    tarjeta_balance = ft.Container(
        width=350,
        height=180,
        border_radius=25,
        padding=25,

        gradient=ft.LinearGradient(
            begin=ft.alignment.Alignment(-1, -1),
            end=ft.alignment.Alignment(1, 1),
            colors=[
                ft.Colors.CYAN_700,
                ft.Colors.BLUE_900
            ]
        ),

        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Icon(
                    ft.Icons.ACCOUNT_BALANCE_WALLET,
                    size=55,
                    color=ft.Colors.WHITE
                ),

                ft.Container(height=10),

                ft.Text(
                    "Gestor Financiero",
                    size=26,
                    weight="bold",
                    color=ft.Colors.WHITE
                ),

                ft.Text(
                    "Administra tus ingresos y gastos",
                    color=ft.Colors.WHITE70,
                    text_align=ft.TextAlign.CENTER
                )
            ]
        )
    )


    acciones = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,

        controls=[

            ft.Container(
                width=100,
                height=100,
                bgcolor=ft.Colors.BLUE_GREY_800,
                border_radius=20,

                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    controls=[

                        ft.Icon(
                            ft.Icons.ADD_CIRCLE,
                            size=40,
                            color=ft.Colors.GREEN_400
                        ),

                        ft.Text(
                            "Ingresos",
                            color=ft.Colors.WHITE
                        )
                    ]
                )
            ),

            ft.Container(
                width=100,
                height=100,
                bgcolor=ft.Colors.BLUE_GREY_800,
                border_radius=20,

                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    controls=[

                        ft.Icon(
                            ft.Icons.REMOVE_CIRCLE,
                            size=40,
                            color=ft.Colors.RED_400
                        ),

                        ft.Text(
                            "Gastos",
                            color=ft.Colors.WHITE
                        )
                    ]
                )
            ),

            ft.Container(
                width=100,
                height=100,
                bgcolor=ft.Colors.BLUE_GREY_800,
                border_radius=20,

                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    controls=[

                        ft.Icon(
                            ft.Icons.PIE_CHART,
                            size=40,
                            color=ft.Colors.CYAN_300
                        ),

                        ft.Text(
                            "Reportes",
                            color=ft.Colors.WHITE
                        )
                    ]
                )
            )
        ]
    )



    panel_info = ft.Container(

        width=350,

        padding=25,

        border_radius=20,

        bgcolor=ft.Colors.BLUE_GREY_800,

        content=ft.Column(

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Icon(
                    ft.Icons.INSIGHTS,
                    size=70,
                    color=ft.Colors.CYAN_300
                ),

                ft.Container(height=10),

                ft.Text(
                    "Aún no tienes movimientos",
                    size=22,
                    weight="bold",
                    color=ft.Colors.WHITE
                ),

                ft.Text(
                    "Comienza agregando ingresos y gastos "
                    "para visualizar estadísticas y reportes.",
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.WHITE70
                )
            ]
        )
    )



    contenido = ft.Column(

        horizontal_alignment=ft.CrossAxisAlignment.CENTER,

        controls=[

            ft.Container(height=20),

            # HEADER
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                controls=[

                    ft.Column(
                        spacing=3,

                        controls=[

                            ft.Text(
                                f"Hola, {usuario['nombre']}",
                                size=28,
                                weight="bold",
                                color=ft.Colors.WHITE
                            ),

                            ft.Text(
                                "Bienvenido nuevamente",
                                color=ft.Colors.WHITE70
                            )
                        ]
                    ),

                    ft.IconButton(
                        icon=ft.Icons.PERSON,
                        icon_color=ft.Colors.CYAN_300,
                        icon_size=35,
                        tooltip="Mi Perfil",
                        on_click=ir_perfil
                    )
                ]
            ),

            ft.Container(height=25),

            
            tarjeta_balance,

            ft.Container(height=30),

          
            acciones,

            ft.Container(height=35),

            
            panel_info,

            ft.Container(height=40),

    
            ft.ElevatedButton(
                "Mi Perfil",
                width=300,
                height=50,
                icon=ft.Icons.PERSON,
                bgcolor=ft.Colors.CYAN_700,
                color=ft.Colors.WHITE,
                on_click=ir_perfil
            ),

            # LOGOUT
            ft.ElevatedButton(
                "Cerrar sesión",
                width=300,
                height=50,
                icon=ft.Icons.LOGOUT,
                bgcolor=ft.Colors.RED_700,
                color=ft.Colors.WHITE,
                on_click=cerrar_sesion
            ),

            ft.Container(height=30)
        ]
    )


    return ft.View(

        route="/dashboard",

        bgcolor=ft.Colors.BLUE_GREY_900,

        appbar=ft.AppBar(
            title=ft.Text("Dashboard Financiero"),
            center_title=True,
            bgcolor=ft.Colors.BLUE_GREY_900
        ),

        controls=[

            ft.Container(
                expand=True,
                padding=20,

                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,

                    controls=[
                        contenido
                    ]
                )
            )
        ]
    )