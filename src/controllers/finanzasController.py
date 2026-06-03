from models.finanzasModel import FinanzasModel

class FinanzasController:
    def __init__(self):
        self.model = FinanzasModel()

    def listar_categorias(self, tipo):
        return self.model.obtener_categorias_por_tipo(tipo)

    def obtener_totales(self, id_usuario):
        return self.model.obtener_resumen_financiero(id_usuario)

    def obtener_historial(self, id_usuario):
        return self.model.obtener_historial_reciente(id_usuario)

    def listar_presupuestos(self, id_usuario):
        return self.model.obtener_presupuestos_con_progreso(id_usuario)

    def eliminar_presupuesto(self, id_p):
        return self.model.borrar_presupuesto(id_p)

    def listar_metas(self, id_usuario):
        return self.model.obtener_metas(id_usuario)

    def eliminar_meta(self, id_m):
        return self.model.borrar_meta(id_m)

    def verificar_bloqueo(self, id_usuario, password):
        if not password:
            return False, "Contraseña requerida."
        if self.model.verificar_password_usuario(id_usuario, password.strip()):
            return True, "Desbloqueado."
        return False, "Contraseña incorrecta."

    def agregar_movimiento(self, id_usuario, id_categoria, monto, descripcion):
        if not id_categoria or not monto or not descripcion:
            return False, "Todos los campos son requeridos."
        try:
            monto_float = float(monto.replace(",", "."))
            if monto_float <= 0:
                return False, "El monto debe ser mayor a cero."
        except ValueError:
            return False, "El monto debe ser un número válido."
        return self.model.insertar_transaccion_con_validacion(id_usuario, id_categoria, monto_float, descripcion)

    def asignar_presupuesto(self, id_usuario, id_categoria, monto_limite):
        if not id_categoria or not monto_limite:
            return False, "Todos los campos son requeridos."
        try:
            monto_float = float(monto_limite.replace(",", "."))
            if monto_float <= 0:
                return False, "El límite debe ser mayor a cero."
        except ValueError:
            return False, "El monto debe ser un número válido."
        return self.model.insertar_presupuesto(id_usuario, id_categoria, monto_float)

    def crear_meta_ahorro(self, id_usuario, nombre_meta, monto_objetivo, fecha_limite):
        if not nombre_meta or not monto_objetivo or not fecha_limite:
            return False, "Todos los campos son requeridos."
        try:
            monto_float = float(monto_objetivo.replace(",", "."))
            if monto_float <= 0:
                return False, "El objetivo debe ser mayor a cero."
        except ValueError:
            return False, "El monto debe ser un número válido."
        return self.model.insertar_meta(id_usuario, nombre_meta, monto_float, fecha_limite)

    def abonar_a_meta(self, id_meta, cantidad):
        if not cantidad:
            return False, "Ingresa una cantidad."
        try:
            cantidad_float = float(cantidad.replace(",", "."))
            if cantidad_float <= 0:
                return False, "La cantidad debe ser mayor a cero."
        except ValueError:
            return False, "La cantidad debe ser un número válido."
        return self.model.abonar_meta(id_meta, cantidad_float)