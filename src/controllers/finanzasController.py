from models.finanzasModel import FinanzasModel

class FinanzasController:
    def __init__(self):
        self.model = FinanzasModel()

    def listar_categorias(self, tipo):
        return self.model.obtener_categorias_por_tipo(tipo)

    def agregar_movimiento(self, id_usuario, id_categoria, monto_str, descripcion):
        if not id_categoria or not monto_str:
            return False, "Por favor, completa los campos obligatorios."
        try:
            monto = float(monto_str)
            if monto <= 0:
                return False, "El monto debe ser mayor a cero."
        except ValueError:
            return False, "El monto ingresado no es válido."

        desc = descripcion.strip() if descripcion else "Sin descripción"
        
        exito = self.model.registrar_transaccion(id_usuario, id_categoria, monto, desc)
        if exito:
            return True, "¡Movimiento guardado con éxito!"
        return False, "Error interno al guardar en la base de datos."

    def obtener_totales(self, id_usuario):
        return self.model.obtener_resumen_financiero(id_usuario)

    def obtener_historial(self, id_usuario):
        return self.model.obtener_historial_reciente(id_usuario)