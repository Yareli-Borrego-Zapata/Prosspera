from .databaseModel import Database

class FinanzasModel:
    def __init__(self):
        self.db = Database()

    def obtener_categorias_por_tipo(self, tipo):
        """Devuelve las categorías filtradas por 'Ingreso' o 'Gasto'"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id_categoria, nombre_categoria FROM categorias WHERE tipo = %s",
            (tipo,)
        )
        categorias = cursor.fetchall()
        conn.close()
        return categorias

    def registrar_transaccion(self, id_usuario, id_categoria, monto, descripcion):
        """Inserta un nuevo movimiento en la tabla transacciones"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO transacciones (id_usuario, id_categoria, monto, descripcion, fecha)
                VALUES (%s, %s, %s, %s, NOW())
                """,
                (id_usuario, id_categoria, monto, descripcion)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al registrar transacción: {e}")
            return False
        finally:
            conn.close()

    def obtener_resumen_financiero(self, id_usuario):
        """Calcula el total de ingresos, gastos y balance neto del usuario"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                SUM(CASE WHEN c.tipo = 'Ingreso' THEN t.monto ELSE 0 END) as total_ingresos,
                SUM(CASE WHEN c.tipo = 'Gasto' THEN t.monto ELSE 0 END) as total_gastos
            FROM transacciones t
            JOIN categorias c ON t.id_categoria = c.id_categoria
            WHERE t.id_usuario = %s
        """
        cursor.execute(query, (id_usuario,))
        resumen = cursor.fetchone()
        conn.close()

        ingresos = float(resumen['total_ingresos'] or 0.0)
        gastos = float(resumen['total_gastos'] or 0.0)
        balance = ingresos - gastos

        return {
            "ingresos": ingresos,
            "gastos": gastos,
            "balance": balance
        }

    def obtener_historial_reciente(self, id_usuario):
        """Obtiene las últimas transacciones registradas por el usuario"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT t.monto, t.descripcion, t.fecha, c.nombre_categoria, c.tipo
            FROM transacciones t
            JOIN categorias c ON t.id_categoria = c.id_categoria
            WHERE t.id_usuario = %s
            ORDER BY t.id_transaccion DESC
            LIMIT 10
        """
        cursor.execute(query, (id_usuario,))
        historial = cursor.fetchall()
        conn.close()
        return historial