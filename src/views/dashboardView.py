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

    esta_bloqueado = False

    txt_balance = ft.Text("$0.00", size=36, weight="bold", color=ft.Colors.WHITE)
    txt_subtitulo = ft.Text("Cargando...", color=ft.Colors.WHITE70, size=13, text_align=ft.TextAlign.CENTER)

    tarjeta_balance = ft.Container(
        width=370, height=190, border_radius=28, padding=30,
        gradient=ft.LinearGradient(
            begin=ft.alignment.Alignment(-1, -1),
            end=ft.alignment.Alignment(1, 1),
            colors=[ft.Colors.CYAN_600, ft.Colors.BLUE_900]
        ),
        shadow=ft.BoxShadow(blur_radius=25, color=ft.Colors.BLACK45, offset=ft.Offset(0, 8)),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=22, color=ft.Colors.WHITE70),
                        ft.Text("Balance Total", size=14, color=ft.Colors.WHITE70),
                    ],
                    spacing=6
                ),
                txt_balance,
                txt_subtitulo,
            ]
        )
    )

    lista_movimientos = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8)
    panel_info = ft.Container(
        width=370, padding=20, border_radius=20,
        bgcolor=ft.Colors.BLUE_GREY_800,
        border=ft.Border(
            top=ft.BorderSide(1, ft.Colors.CYAN_900),
            bottom=ft.BorderSide(1, ft.Colors.CYAN_900),
            left=ft.BorderSide(1, ft.Colors.CYAN_900),
            right=ft.BorderSide(1, ft.Colors.CYAN_900),
        ),
        content=lista_movimientos
    )

    lista_presupuestos = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.START, spacing=10)
    panel_presupuestos = ft.Container(
        width=370, padding=20, border_radius=20,
        bgcolor=ft.Colors.BLUE_GREY_800,
        border=ft.Border(
            top=ft.BorderSide(1, ft.Colors.CYAN_900),
            bottom=ft.BorderSide(1, ft.Colors.CYAN_900),
            left=ft.BorderSide(1, ft.Colors.CYAN_900),
            right=ft.BorderSide(1, ft.Colors.CYAN_900),
        ),
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.TRACK_CHANGES, color=ft.Colors.CYAN_400, size=18),
                ft.Text("Límites de Presupuesto", size=15, weight="bold", color=ft.Colors.CYAN_100),
            ], spacing=8),
            ft.Divider(height=1, color=ft.Colors.BLUE_GREY_700),
            lista_presupuestos
        ], spacing=10)
    )

    lista_metas = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.START, spacing=10)
    panel_metas = ft.Container(
        width=370, padding=20, border_radius=20,
        bgcolor=ft.Colors.BLUE_GREY_800,
        border=ft.Border(
            top=ft.BorderSide(1, ft.Colors.CYAN_900),
            bottom=ft.BorderSide(1, ft.Colors.CYAN_900),
            left=ft.BorderSide(1, ft.Colors.CYAN_900),
            right=ft.BorderSide(1, ft.Colors.CYAN_900),
        ),
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.FLAG_ROUNDED, color=ft.Colors.AMBER_400, size=18),
                ft.Text("Metas de Ahorro", size=15, weight="bold", color=ft.Colors.CYAN_100),
            ], spacing=8),
            ft.Divider(height=1, color=ft.Colors.BLUE_GREY_700),
            lista_metas
        ], spacing=10)
    )

    input_seguridad = ft.TextField(
        label="Contraseña para desbloquear",
        password=True, can_reveal_password=True,
        border_color=ft.Colors.CYAN_400,
        focused_border_color=ft.Colors.CYAN_300,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_GREY_900,
        border_radius=12,
        width=290,
        cursor_color=ft.Colors.CYAN_400,
        label_style=ft.TextStyle(color=ft.Colors.CYAN_200),
    )

    def ejecutar_desbloqueo(e):
        nonlocal esta_bloqueado
        valido, msg = finanzas_ctrl.verificar_bloqueo(usuario['id_usuario'], input_seguridad.value)
        if valido:
            esta_bloqueado = False
            input_seguridad.value = ""
            btn_candado.icon = ft.Icons.LOCK_OPEN_ROUNDED
            btn_candado.icon_color = ft.Colors.GREEN_400
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.GREEN)
            page.snack_bar.open = True
            actualizar_pantalla()
        else:
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.RED_400)
            page.snack_bar.open = True
            page.update()

    panel_bloqueo_seguro = ft.Container(
        width=370, padding=30, border_radius=25,
        bgcolor=ft.Colors.BLUE_GREY_800,
        border=ft.Border(
            top=ft.BorderSide(1, ft.Colors.CYAN_900),
            bottom=ft.BorderSide(1, ft.Colors.CYAN_900),
            left=ft.BorderSide(1, ft.Colors.CYAN_900),
            right=ft.BorderSide(1, ft.Colors.CYAN_900),
        ),
        alignment=ft.alignment.Alignment(0, 0),
        content=ft.Column([
            ft.Container(
                width=70, height=70, border_radius=35,
                bgcolor=ft.Colors.CYAN_900,
                content=ft.Icon(ft.Icons.SHIELD_ROUNDED, size=35, color=ft.Colors.CYAN_300),
                alignment=ft.alignment.Alignment(0, 0),
            ),
            ft.Text("Vista Protegida", size=18, weight="bold", color=ft.Colors.WHITE),
            ft.Text(
                "Ingresa tu contraseña para continuar.",
                color=ft.Colors.WHITE54, text_align=ft.TextAlign.CENTER, size=13
            ),
            ft.Container(height=5),
            input_seguridad,
            ft.ElevatedButton(
                "Desbloquear", on_click=ejecutar_desbloqueo,
                width=290, height=45,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.CYAN_700,
                    color=ft.Colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=12),
                )
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=14)
    )

    def actualizar_pantalla():
        panel_bloqueo_seguro.visible = esta_bloqueado
        acciones.visible = not esta_bloqueado
        panel_info.visible = not esta_bloqueado
        panel_presupuestos.visible = not esta_bloqueado
        panel_metas.visible = not esta_bloqueado
        tarjeta_balance.visible = not esta_bloqueado
        btn_perfil_icono.visible = not esta_bloqueado
        btn_perfil_abajo.visible = not esta_bloqueado
        btn_cerrar_sesion.visible = not esta_bloqueado

        if esta_bloqueado:
            page.update()
            return

        totales = finanzas_ctrl.obtener_totales(usuario['id_usuario'])
        txt_balance.value = f"${totales['balance']:.2f}"
        txt_subtitulo.value = f"↑ ${totales['ingresos']:.2f}   |   ↓ ${totales['gastos']:.2f}"

        historial = finanzas_ctrl.obtener_historial(usuario['id_usuario'])
        lista_movimientos.controls.clear()
        if not historial:
            lista_movimientos.controls.extend([
                ft.Container(height=10),
                ft.Icon(ft.Icons.INSIGHTS, size=50, color=ft.Colors.CYAN_800),
                ft.Text("Sin movimientos aún", size=16, weight="bold", color=ft.Colors.WHITE70),
                ft.Text("Agrega ingresos o gastos para empezar.", size=13,
                        text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE38),
                ft.Container(height=10),
            ])
        else:
            lista_movimientos.controls.append(
                ft.Row([
                    ft.Icon(ft.Icons.RECEIPT_LONG, color=ft.Colors.CYAN_400, size=18),
                    ft.Text("Últimos Movimientos", size=15, weight="bold", color=ft.Colors.CYAN_100),
                ], spacing=8)
            )
            lista_movimientos.controls.append(ft.Divider(height=1, color=ft.Colors.BLUE_GREY_700))
            for m in historial:
                es_ingreso = m['tipo'] == 'Ingreso'
                color_monto = ft.Colors.GREEN_400 if es_ingreso else ft.Colors.RED_400
                signo = "+" if es_ingreso else "-"
                icono = ft.Icons.ARROW_UPWARD if es_ingreso else ft.Icons.ARROW_DOWNWARD
                lista_movimientos.controls.append(
                    ft.Container(
                        padding=10, border_radius=12, bgcolor=ft.Colors.BLUE_GREY_900,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row([
                                    ft.Container(
                                        width=36, height=36, border_radius=18,
                                        bgcolor=ft.Colors.BLUE_GREY_800,
                                        content=ft.Icon(icono, color=color_monto, size=18),
                                        alignment=ft.alignment.Alignment(0, 0),
                                    ),
                                    ft.Column([
                                        ft.Text(m['descripcion'], size=13, weight="bold",
                                                color=ft.Colors.WHITE, max_lines=1),
                                        ft.Text(m['nombre_categoria'], size=11, color=ft.Colors.WHITE54),
                                    ], spacing=1)
                                ], spacing=10),
                                ft.Text(f"{signo}${float(m['monto']):.2f}", size=14,
                                        weight="bold", color=color_monto)
                            ]
                        )
                    )
                )

        presupuestos = finanzas_ctrl.listar_presupuestos(usuario['id_usuario'])
        lista_presupuestos.controls.clear()
        if not presupuestos:
            lista_presupuestos.controls.append(
                ft.Text("Sin presupuestos este mes.", color=ft.Colors.WHITE54, size=13)
            )
        else:
            for p in presupuestos:
                limite = float(p['monto_limite'])
                gastado = float(p['monto_gastado'])
                progreso = min(gastado / limite, 1.0) if limite > 0 else 0.0
                color_barra = ft.Colors.CYAN_400 if progreso < 0.9 else ft.Colors.RED_400

                def click_borrar_p(id_presupuesto_click):
                    return lambda _: ejecutar_eliminar_presupuesto(id_presupuesto_click)

                lista_presupuestos.controls.append(
                    ft.Container(
                        padding=10, border_radius=12, bgcolor=ft.Colors.BLUE_GREY_900,
                        content=ft.Column([
                            ft.Row([
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED_400,
                                        icon_size=16, tooltip="Eliminar límite",
                                        on_click=click_borrar_p(p['id_presupuesto'])
                                    ),
                                    ft.Text(p['nombre_categoria'], color=ft.Colors.WHITE,
                                            weight="bold", size=13),
                                ]),
                                ft.Text(f"${gastado:.2f} / ${limite:.2f}", color=ft.Colors.WHITE54, size=12)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.ProgressBar(value=progreso, color=color_barra,
                                           bgcolor=ft.Colors.BLUE_GREY_800, height=7, border_radius=5)
                        ], spacing=6)
                    )
                )

        metas = finanzas_ctrl.listar_metas(usuario['id_usuario'])
        lista_metas.controls.clear()
        if not metas:
            lista_metas.controls.append(
                ft.Text("No tienes metas activas.", color=ft.Colors.WHITE54, size=13)
            )
        else:
            for m in metas:
                objetivo = float(m['monto_objetivo'])
                actual = float(m['monto_actual'])
                progreso = min(actual / objetivo, 1.0) if objetivo > 0 else 0.0

                def click_abonar(id_meta_click):
                    return lambda _: abrir_modal_abonar_meta(id_meta_click)

                def click_borrar_m(id_meta_click):
                    return lambda _: ejecutar_eliminar_meta(id_meta_click)

                lista_metas.controls.append(
                    ft.Container(
                        padding=10, border_radius=12, bgcolor=ft.Colors.BLUE_GREY_900,
                        content=ft.Column([
                            ft.Row([
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED_400,
                                        icon_size=16, tooltip="Eliminar meta",
                                        on_click=click_borrar_m(m['id_meta'])
                                    ),
                                    ft.Column([
                                        ft.Text(m['nombre_meta'], color=ft.Colors.WHITE,
                                                weight="bold", size=13),
                                        ft.Text(f"${actual:.2f} de ${objetivo:.2f}",
                                                color=ft.Colors.WHITE54, size=12),
                                    ], spacing=1),
                                ]),
                                ft.IconButton(
                                    icon=ft.Icons.PRICE_CHECK, icon_color=ft.Colors.GREEN_400,
                                    icon_size=22, tooltip="Abonar",
                                    on_click=click_abonar(m['id_meta'])
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.ProgressBar(value=progreso, color=ft.Colors.GREEN_400,
                                           bgcolor=ft.Colors.BLUE_GREY_800, height=7, border_radius=5)
                        ], spacing=6)
                    )
                )

        page.update()

    def ejecutar_eliminar_presupuesto(id_presupuesto):
        if finanzas_ctrl.eliminar_presupuesto(id_presupuesto):
            page.snack_bar = ft.SnackBar(ft.Text("Presupuesto eliminado."), bgcolor=ft.Colors.GREEN)
            page.snack_bar.open = True
            actualizar_pantalla()

    def ejecutar_eliminar_meta(id_meta):
        if finanzas_ctrl.eliminar_meta(id_meta):
            page.snack_bar = ft.SnackBar(ft.Text("Meta eliminada."), bgcolor=ft.Colors.GREEN)
            page.snack_bar.open = True
            actualizar_pantalla()

    def cambiar_estado_seguridad(e):
        nonlocal esta_bloqueado
        if not esta_bloqueado:
            esta_bloqueado = True
            btn_candado.icon = ft.Icons.LOCK_ROUNDED
            btn_candado.icon_color = ft.Colors.RED_400
            page.snack_bar = ft.SnackBar(
                ft.Text("Vista bloqueada."), bgcolor=ft.Colors.BLUE_GREY_700
            )
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Ingresa tu contraseña para desbloquear."), bgcolor=ft.Colors.ORANGE_700
            )
            page.snack_bar.open = True
        actualizar_pantalla()

    btn_candado = ft.IconButton(
        icon=ft.Icons.LOCK_OPEN_ROUNDED, icon_color=ft.Colors.GREEN_400,
        icon_size=24, tooltip="Proteger pantalla", on_click=cambiar_estado_seguridad
    )
    btn_perfil_icono = ft.IconButton(
        icon=ft.Icons.PERSON_ROUNDED, icon_color=ft.Colors.CYAN_300,
        icon_size=28, tooltip="Mi Perfil", on_click=ir_perfil
    )
    btn_perfil_abajo = ft.ElevatedButton(
        "Mi Perfil", width=370, height=48, icon=ft.Icons.PERSON_ROUNDED,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_GREY_700,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        on_click=ir_perfil
    )
    btn_cerrar_sesion = ft.ElevatedButton(
        "Cerrar sesión", width=370, height=48, icon=ft.Icons.LOGOUT_ROUNDED,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.RED_900,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        on_click=cerrar_sesion
    )

    def abrir_modal_movimiento(tipo_movimiento):
        categorias = finanzas_ctrl.listar_categorias(tipo_movimiento)
        input_monto = ft.TextField(label="Monto ($)", keyboard_type=ft.KeyboardType.NUMBER,
                                   border_color=ft.Colors.CYAN_400, color=ft.Colors.WHITE,
                                   bgcolor=ft.Colors.BLUE_GREY_900, border_radius=10)
        input_desc = ft.TextField(label="Descripción", border_color=ft.Colors.CYAN_400,
                                  color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_GREY_900, border_radius=10)
        dropdown_cat = ft.Dropdown(
            label="Categoría", border_color=ft.Colors.CYAN_400, color=ft.Colors.WHITE,
            options=[ft.dropdown.Option(str(c['id_categoria']), c['nombre_categoria']) for c in categorias]
        )

        def guardar_click(e):
            exito, msg = finanzas_ctrl.agregar_movimiento(
                usuario['id_usuario'], dropdown_cat.value, input_monto.value, input_desc.value
            )
            if exito:
                dialog.open = False
                bg_snack = ft.Colors.ORANGE_700 if "⚠️" in msg else ft.Colors.GREEN
                page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=bg_snack)
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
                ft.TextButton("Cancelar",
                              on_click=lambda _: setattr(dialog, "open", False) or page.update(),
                              style=ft.ButtonStyle(color=ft.Colors.WHITE60)),
                ft.ElevatedButton("Guardar", on_click=guardar_click,
                                  style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_600, color=ft.Colors.WHITE))
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def abrir_modal_presupuesto():
        categorias = finanzas_ctrl.listar_categorias("Gasto")
        input_limite = ft.TextField(label="Límite Mensual ($)", keyboard_type=ft.KeyboardType.NUMBER,
                                    border_color=ft.Colors.CYAN_400, color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.BLUE_GREY_900, border_radius=10)
        dropdown_cat = ft.Dropdown(
            label="Categoría de Gasto", border_color=ft.Colors.CYAN_400, color=ft.Colors.WHITE,
            options=[ft.dropdown.Option(str(c['id_categoria']), c['nombre_categoria']) for c in categorias]
        )

        def guardar_presupuesto_click(e):
            exito, msg = finanzas_ctrl.asignar_presupuesto(
                usuario['id_usuario'], dropdown_cat.value, input_limite.value
            )
            if exito:
                dialog_p.open = False
                page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.GREEN)
                page.snack_bar.open = True
                actualizar_pantalla()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.RED_400)
                page.snack_bar.open = True
                page.update()

        dialog_p = ft.AlertDialog(
            title=ft.Text("Definir Presupuesto", color=ft.Colors.WHITE, weight="bold"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            content=ft.Column([dropdown_cat, input_limite], tight=True, spacing=15),
            actions=[
                ft.TextButton("Cancelar",
                              on_click=lambda _: setattr(dialog_p, "open", False) or page.update(),
                              style=ft.ButtonStyle(color=ft.Colors.WHITE60)),
                ft.ElevatedButton("Establecer", on_click=guardar_presupuesto_click,
                                  style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_600, color=ft.Colors.WHITE))
            ]
        )
        page.overlay.append(dialog_p)
        dialog_p.open = True
        page.update()

    def abrir_modal_meta():
        input_nombre = ft.TextField(label="¿Para qué vas a ahorrar?",
                                    border_color=ft.Colors.CYAN_400, color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.BLUE_GREY_900, border_radius=10)
        input_objetivo = ft.TextField(label="Monto Objetivo ($)", keyboard_type=ft.KeyboardType.NUMBER,
                                      border_color=ft.Colors.CYAN_400, color=ft.Colors.WHITE,
                                      bgcolor=ft.Colors.BLUE_GREY_900, border_radius=10)
        input_fecha = ft.TextField(label="Fecha Límite (AAAA-MM-DD)", value="2026-12-31",
                                   border_color=ft.Colors.CYAN_400, color=ft.Colors.WHITE,
                                   bgcolor=ft.Colors.BLUE_GREY_900, border_radius=10)

        def guardar_meta_click(e):
            exito, msg = finanzas_ctrl.crear_meta_ahorro(
                usuario['id_usuario'], input_nombre.value, input_objetivo.value, input_fecha.value
            )
            if exito:
                dialog_m.open = False
                page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.GREEN)
                page.snack_bar.open = True
                actualizar_pantalla()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.RED_400)
                page.snack_bar.open = True
                page.update()

        dialog_m = ft.AlertDialog(
            title=ft.Text("Nueva Meta de Ahorro", color=ft.Colors.WHITE, weight="bold"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            content=ft.Column([input_nombre, input_objetivo, input_fecha], tight=True, spacing=15),
            actions=[
                ft.TextButton("Cancelar",
                              on_click=lambda _: setattr(dialog_m, "open", False) or page.update(),
                              style=ft.ButtonStyle(color=ft.Colors.WHITE60)),
                ft.ElevatedButton("Crear Meta", on_click=guardar_meta_click,
                                  style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_600, color=ft.Colors.WHITE))
            ]
        )
        page.overlay.append(dialog_m)
        dialog_m.open = True
        page.update()

    def abrir_modal_abonar_meta(id_meta):
        input_abono = ft.TextField(label="Cantidad a agregar ($)", keyboard_type=ft.KeyboardType.NUMBER,
                                   border_color=ft.Colors.GREEN_400, color=ft.Colors.WHITE,
                                   bgcolor=ft.Colors.BLUE_GREY_900, border_radius=10)

        def guardar_abono_click(e):
            exito, msg = finanzas_ctrl.abonar_a_meta(id_meta, input_abono.value)
            if exito:
                dialog_a.open = False
                page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.GREEN)
                page.snack_bar.open = True
                actualizar_pantalla()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.RED_400)
                page.snack_bar.open = True
                page.update()

        dialog_a = ft.AlertDialog(
            title=ft.Text("Abonar a tu Ahorro", color=ft.Colors.WHITE, weight="bold"),
            bgcolor=ft.Colors.BLUE_GREY_900,
            content=ft.Column([input_abono], tight=True, spacing=15),
            actions=[
                ft.TextButton("Cancelar",
                              on_click=lambda _: setattr(dialog_a, "open", False) or page.update(),
                              style=ft.ButtonStyle(color=ft.Colors.WHITE60)),
                ft.ElevatedButton("Abonar", on_click=guardar_abono_click,
                                  style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE))
            ]
        )
        page.overlay.append(dialog_a)
        dialog_a.open = True
        page.update()

    acciones = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER, spacing=12,
        controls=[
            ft.Container(
                width=82, height=90, border_radius=18,
                bgcolor=ft.Colors.BLUE_GREY_800,
                border=ft.Border(
                    top=ft.BorderSide(1, ft.Colors.GREEN_900),
                    bottom=ft.BorderSide(1, ft.Colors.GREEN_900),
                    left=ft.BorderSide(1, ft.Colors.GREEN_900),
                    right=ft.BorderSide(1, ft.Colors.GREEN_900),
                ),
                on_click=lambda _: abrir_modal_movimiento("Ingreso"),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                    controls=[
                        ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, size=28, color=ft.Colors.GREEN_400),
                        ft.Text("Ingresos", color=ft.Colors.WHITE70, size=11)
                    ]
                )
            ),
            ft.Container(
                width=82, height=90, border_radius=18,
                bgcolor=ft.Colors.BLUE_GREY_800,
                border=ft.Border(
                    top=ft.BorderSide(1, ft.Colors.RED_900),
                    bottom=ft.BorderSide(1, ft.Colors.RED_900),
                    left=ft.BorderSide(1, ft.Colors.RED_900),
                    right=ft.BorderSide(1, ft.Colors.RED_900),
                ),
                on_click=lambda _: abrir_modal_movimiento("Gasto"),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                    controls=[
                        ft.Icon(ft.Icons.REMOVE_CIRCLE_OUTLINE, size=28, color=ft.Colors.RED_400),
                        ft.Text("Gastos", color=ft.Colors.WHITE70, size=11)
                    ]
                )
            ),
            ft.Container(
                width=82, height=90, border_radius=18,
                bgcolor=ft.Colors.BLUE_GREY_800,
                border=ft.Border(
                    top=ft.BorderSide(1, ft.Colors.CYAN_900),
                    bottom=ft.BorderSide(1, ft.Colors.CYAN_900),
                    left=ft.BorderSide(1, ft.Colors.CYAN_900),
                    right=ft.BorderSide(1, ft.Colors.CYAN_900),
                ),
                on_click=lambda _: abrir_modal_presupuesto(),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                    controls=[
                        ft.Icon(ft.Icons.TRACK_CHANGES, size=28, color=ft.Colors.CYAN_300),
                        ft.Text("Límites", color=ft.Colors.WHITE70, size=11)
                    ]
                )
            ),
            ft.Container(
                width=82, height=90, border_radius=18,
                bgcolor=ft.Colors.BLUE_GREY_800,
                border=ft.Border(
                    top=ft.BorderSide(1, ft.Colors.AMBER_900),
                    bottom=ft.BorderSide(1, ft.Colors.AMBER_900),
                    left=ft.BorderSide(1, ft.Colors.AMBER_900),
                    right=ft.BorderSide(1, ft.Colors.AMBER_900),
                ),
                on_click=lambda _: abrir_modal_meta(),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                    controls=[
                        ft.Icon(ft.Icons.FLAG_ROUNDED, size=28, color=ft.Colors.AMBER_400),
                        ft.Text("Metas", color=ft.Colors.WHITE70, size=11)
                    ]
                )
            ),
        ]
    )

    inicial = usuario['nombre'][0].upper()

    contenido_principal = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        controls=[
            ft.Container(height=10),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column([
                        ft.Text(f"Hola, {usuario['nombre']}", size=22, weight="bold", color=ft.Colors.WHITE),
                        ft.Text("Bienvenido a PROSSPERA", color=ft.Colors.WHITE54, size=13)
                    ], spacing=2),
                    ft.Row([
                        btn_candado,
                        ft.Container(
                            width=38, height=38, border_radius=19,
                            bgcolor=ft.Colors.CYAN_900,
                            content=ft.Text(inicial, size=16, weight="bold", color=ft.Colors.WHITE),
                            alignment=ft.alignment.Alignment(0, 0),
                            on_click=ir_perfil,
                            tooltip="Mi Perfil",
                        )
                    ], spacing=4)
                ]
            ),
            ft.Container(height=20),
            panel_bloqueo_seguro,
            tarjeta_balance,
            ft.Container(height=20),
            acciones,
            ft.Container(height=20),
            panel_info,
            ft.Container(height=16),
            panel_presupuestos,
            ft.Container(height=16),
            panel_metas,
            ft.Container(height=30),
            btn_perfil_abajo,
            ft.Container(height=8),
            btn_cerrar_sesion,
            ft.Container(height=30)
        ]
    )

    # Reemplazamos btn_perfil_icono por el avatar, pero lo dejamos definido para el visible toggle
    btn_perfil_icono = ft.Container(width=0, height=0, visible=True)

    actualizar_pantalla()

    return ft.View(
        route="/dashboard",
        bgcolor=ft.Colors.BLUE_GREY_900,
        appbar=ft.AppBar(
            title=ft.Text("PROSSPERA", size=20, weight="bold", color=ft.Colors.WHITE),
            center_title=True,
            bgcolor=ft.Colors.BLUE_GREY_900,
            elevation=0,
        ),
        controls=[ft.Container(
            expand=True, padding=20,
            content=ft.Column(scroll=ft.ScrollMode.AUTO, controls=[contenido_principal])
        )]
    )