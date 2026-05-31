import flet as ft
from controllers.finanzasController import FinanzasController

def DashboardView(page: ft.Page):
    usuario = page.user_data
    finanzas_ctrl = FinanzasController()

    def ir_perfil(e):
        page.go("/profile")

    def cerrar_sesion(e):
        page.user_data = None
        page.go("/")

    txt_balance = ft.Text("$0.00", size=32, weight="bold", color=ft.Colors.WHITE)
    txt_subtitulo = ft.Text("Cargando tus finanzas...", color=ft.Colors.WHITE70, text_align=ft.TextAlign.CENTER)

    tarjeta_balance = ft.Container(
        width=350,
        height=180,
        border_radius=25,
        padding=25,
        gradient=ft.LinearGradient(
            begin=ft.alignment.Alignment(-1, -1),
            end=ft.alignment.Alignment(1, 1),
            colors=[ft.Colors.CYAN_700, ft.Colors.BLUE_900]
        ),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=45, color=ft.Colors.WHITE),
                txt_balance,
                txt_subtitulo
            ]
        )
    )


    lista_movimientos = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
    panel_info = ft.Container(
        width=350,
        padding=20,
        border_radius=20,
        bgcolor=ft.Colors.BLUE_GREY_800,
        content=lista_movimientos
    )

    def actualizar_pantalla():
        """Consulta la base de datos y refresca el balance y el historial en la UI"""
        totales = finanzas_ctrl.obtener_totales(usuario['id_usuario'])
        txt_balance.value = f"${totales['balance']:.2f}"
        txt_subtitulo.value = f"Ingresos: ${totales['ingresos']:.2f}  |  Gastos: ${totales['gastos']:.2f}"
        
        historial = finanzas_ctrl.obtener_historial(usuario['id_usuario'])
        lista_movimientos.controls.clear()

        if not historial:
            lista_movimientos.controls.extend([
                ft.Icon(ft.Icons.INSIGHTS, size=60, color=ft.Colors.CYAN_300),
                ft.Container(height=5),
                ft.Text("Aún no tienes movimientos", size=18, weight="bold", color=ft.Colors.WHITE),
                ft.Text("Comienza agregando ingresos y gastos para visualizar estadísticas.", text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE70)
            ])
        else:
            lista_movimientos.controls.append(
                ft.Text("Últimos Movimientos", size=16, weight="bold", color=ft.Colors.CYAN_100)
            )
            for m in historial:
                es_ingreso = m['tipo'] == 'Ingreso'
                color_monto = ft.Colors.GREEN_400 if es_ingreso else ft.Colors.RED_400
                signo = "+" if es_ingreso else "-"
                icono = ft.Icons.ARROW_UPWARD if es_ingreso else ft.Icons.ARROW_DOWNWARD

                lista_movimientos.controls.append(
                    ft.Container(
                        padding=10,
                        border_radius=10,
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row([
                                    ft.Icon(icono, color=color_monto, size=20),
                                    ft.Column([
                                        ft.Text(m['descripcion'], size=14, weight="bold", color=ft.Colors.WHITE, max_lines=1),
                                        ft.Text(m['nombre_categoria'], size=12, color=ft.Colors.WHITE60),
                                    ], spacing=2)
                                ]),
                                ft.Text(f"{signo}${float(m['monto']):.2f}", size=14, weight="bold", color=color_monto)
                            ]
                        )
                    )
                )
        page.update()

    def abrir_modal_movimiento(tipo_movimiento):
        """Genera y abre el AlertDialog dinámico de Flet para capturar datos"""
        categorias = finanzas_ctrl.listar_categorias(tipo_movimiento)
        
        input_monto = ft.TextField(label="Monto ($)", keyboard_type=ft.KeyboardType.NUMBER, border_color=ft.Colors.CYAN_400, color=ft.Colors.WHITE)
        input_desc = ft.TextField(label="Descripción", border_color=ft.Colors.CYAN_400, color=ft.Colors.WHITE)
        
        dropdown_cat = ft.Dropdown(
            label="Categoría",
            border_color=ft.Colors.CYAN_400,
            color=ft.Colors.WHITE,
            options=[ft.dropdown.Option(str(c['id_categoria']), c['nombre_categoria']) for c in categorias]
        )

        def guardar_click(e):
            exito, msg = finanzas_ctrl.agregar_movimiento(
                usuario['id_usuario'],
                dropdown_cat.value,
                input_monto.value,
                input_desc.value
            )
            if exito:
                dialog.open = False
                page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.GREEN)
                page.snack_bar.open = True
                actualizar_pantalla()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.RED_400)
                page.snack_bar.open = True
                page.update()

        dialog = ft.AlertDialog(
            title=ft.Text(f"Añadir {tipo_movimiento}", color=ft.Colors.WHITE, weight="bold"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            content=ft.Column([dropdown_cat, input_monto, input_desc], tight=True, spacing=15),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: setattr(dialog, "open", False) or page.update(), style=ft.ButtonStyle(color=ft.Colors.WHITE60)),
                ft.ElevatedButton("Guardar", on_click=guardar_click, style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_600, color=ft.Colors.WHITE))
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()


    acciones = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
        controls=[
            ft.Container(
                width=100, height=100, bgcolor=ft.Colors.BLUE_GREY_800, border_radius=20,
                on_click=lambda _: abrir_modal_movimiento("Ingreso"),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[ft.Icon(ft.Icons.ADD_CIRCLE, size=40, color=ft.Colors.GREEN_400), ft.Text("Ingresos", color=ft.Colors.WHITE)]
                )
            ),
            ft.Container(
                width=100, height=100, bgcolor=ft.Colors.BLUE_GREY_800, border_radius=20,
                on_click=lambda _: abrir_modal_movimiento("Gasto"),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[ft.Icon(ft.Icons.REMOVE_CIRCLE, size=40, color=ft.Colors.RED_400), ft.Text("Gastos", color=ft.Colors.WHITE)]
                )
            ),
            ft.Container(
                width=100, height=100, bgcolor=ft.Colors.BLUE_GREY_800, border_radius=20,
                on_click=lambda _: page.snack_bar or setattr(page, "snack_bar", ft.SnackBar(ft.Text("Módulo de reportes próximamente."), bgcolor=ft.Colors.CYAN_700)) or setattr(page.snack_bar, "open", True) or page.update(),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[ft.Icon(ft.Icons.PIE_CHART, size=40, color=ft.Colors.CYAN_300), ft.Text("Reportes", color=ft.Colors.WHITE)]
                )
            )
        ]
    )

    contenido = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(height=20),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column([
                        ft.Text(f"Hola, {usuario['nombre']}", size=28, weight="bold", color=ft.Colors.WHITE),
                        ft.Text("Bienvenido nuevamente", color=ft.Colors.WHITE70)
                    ], spacing=3),
                    ft.IconButton(icon=ft.Icons.PERSON, icon_color=ft.Colors.CYAN_300, icon_size=35, tooltip="Mi Perfil", on_click=ir_perfil)
                ]
            ),
            ft.Container(height=25),
            tarjeta_balance,
            ft.Container(height=30),
            acciones,
            ft.Container(height=35),
            panel_info,
            ft.Container(height=40),
            ft.ElevatedButton("Mi Perfil", width=300, height=50, icon=ft.Icons.PERSON, bgcolor=ft.Colors.CYAN_700, color=ft.Colors.WHITE, on_click=ir_perfil),
            ft.ElevatedButton("Cerrar sesión", width=300, height=50, icon=ft.Icons.LOGOUT, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, on_click=cerrar_sesion),
            ft.Container(height=30)
        ]
    )

    actualizar_pantalla()

    return ft.View(
        route="/dashboard",
        bgcolor=ft.Colors.BLUE_GREY_900,
        appbar=ft.AppBar(title=ft.Text("Dashboard Financiero"), center_title=True, bgcolor=ft.Colors.BLUE_GREY_900),
        controls=[ft.Container(expand=True, padding=20, content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[contenido]))]
    )