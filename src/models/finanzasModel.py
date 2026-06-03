from .databaseModel import Database
import bcrypt

class FinanzasModel:
    def __init__(self):
        self.db = Database()

    def obtener_categorias_por_tipo(self, tipo):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_categoria, nombre_categoria FROM categorias WHERE tipo = %s", (tipo,))
        categorias = cursor.fetchall()
        conn.close()
        return categorias

    def registrar_transaccion(self, id_usuario, id_categoria, monto, descripcion):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transacciones (id_usuario, id_categoria, monto, descripcion, fecha) VALUES (%s, %s, %s, %s, NOW())", (id_usuario, id_categoria, monto, descripcion))
        conn.commit()
        conn.close()
        return True

    def obtener_resumen_financiero(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT SUM(CASE WHEN c.tipo = 'Ingreso' THEN t.monto ELSE 0 END) as total_ingresos, SUM(CASE WHEN c.tipo = 'Gasto' THEN t.monto ELSE 0 END) as total_gastos FROM transacciones t JOIN categorias c ON t.id_categoria = c.id_categoria WHERE t.id_usuario = %s", (id_usuario,))
        resumen = cursor.fetchone()
        conn.close()
        ingresos = float(resumen['total_ingresos'] or 0.0)
        gastos = float(resumen['total_gastos'] or 0.0)
        return {"ingresos": ingresos, "gastos": gastos, "balance": ingresos - gastos}

    def obtener_historial_reciente(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT t.monto, t.descripcion, t.fecha, c.nombre_categoria, c.tipo FROM transacciones t JOIN categorias c ON t.id_categoria = c.id_categoria WHERE t.id_usuario = %s ORDER BY t.id_transaccion DESC LIMIT 10", (id_usuario,))
        historial = cursor.fetchall()
        conn.close()
        return historial

    def obtener_presupuestos_con_progreso(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT p.id_presupuesto, p.id_categoria, c.nombre_categoria, p.monto_limite, COALESCE(SUM(t.monto), 0.0) AS monto_gastado FROM presupuestos p JOIN categorias c ON p.id_categoria = c.id_categoria LEFT JOIN transacciones t ON p.id_categoria = t.id_categoria AND t.id_usuario = p.id_usuario WHERE p.id_usuario = %s GROUP BY p.id_presupuesto", (id_usuario,))
        res = cursor.fetchall()
        conn.close()
        return res

    def borrar_presupuesto(self, id_presupuesto):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM presupuestos WHERE id_presupuesto = %s", (id_presupuesto,))
        conn.commit()
        conn.close()
        return True

    def obtener_metas(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM metas_ahorro WHERE id_usuario = %s", (id_usuario,))
        metas = cursor.fetchall()
        conn.close()
        return metas

    def borrar_meta(self, id_meta):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM metas_ahorro WHERE id_meta = %s", (id_meta,))
        conn.commit()
        conn.close()
        return True

    def verificar_password_usuario(self, id_usuario, password):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT password FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return True
        return False

    def insertar_transaccion_con_validacion(self, id_usuario, id_categoria, monto, descripcion):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "INSERT INTO transacciones (id_usuario, id_categoria, monto, descripcion, fecha) VALUES (%s, %s, %s, %s, NOW())",
                (id_usuario, id_categoria, monto, descripcion)
            )
            conn.commit()
            cursor.execute(
                "SELECT p.monto_limite, COALESCE(SUM(t.monto), 0) as gastado FROM presupuestos p LEFT JOIN transacciones t ON p.id_categoria = t.id_categoria AND t.id_usuario = p.id_usuario WHERE p.id_usuario = %s AND p.id_categoria = %s GROUP BY p.monto_limite",
                (id_usuario, id_categoria)
            )
            presupuesto = cursor.fetchone()
            if presupuesto and float(presupuesto['gastado']) >= float(presupuesto['monto_limite']):
                return True, "⚠️ Movimiento guardado, pero superaste el límite de presupuesto."
            return True, "Movimiento guardado correctamente."
        except Exception as e:
            print(f"Error insertando transacción: {e}")
            return False, "Error al guardar el movimiento."
        finally:
            conn.close()

    def insertar_presupuesto(self, id_usuario, id_categoria, monto_limite):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO presupuestos (id_usuario, id_categoria, monto_limite) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE monto_limite = %s",
                (id_usuario, id_categoria, monto_limite, monto_limite)
            )
            conn.commit()
            return True, "Presupuesto establecido correctamente."
        except Exception as e:
            print(f"Error insertando presupuesto: {e}")
            return False, "Error al guardar el presupuesto."
        finally:
            conn.close()

    def insertar_meta(self, id_usuario, nombre_meta, monto_objetivo, fecha_limite):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            print(f"DEBUG insertar_meta → id_usuario={id_usuario}, nombre={nombre_meta}, objetivo={monto_objetivo}, fecha={fecha_limite}")
            cursor.execute(
                "INSERT INTO metas_ahorro (id_usuario, nombre_meta, monto_objetivo, monto_actual, fecha_limite) VALUES (%s, %s, %s, 0, %s)",
                (id_usuario, nombre_meta, monto_objetivo, fecha_limite)
            )
            conn.commit()
            print("DEBUG insertar_meta → INSERT exitoso")
            return True, "Meta de ahorro creada correctamente."
        except Exception as e:
            print(f"ERROR EXACTO insertar_meta: {e}")
            return False, "Error al crear la meta."
        finally:
            conn.close()

    def abonar_meta(self, id_meta, cantidad):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT monto_actual, monto_objetivo FROM metas_ahorro WHERE id_meta = %s", (id_meta,))
            meta = cursor.fetchone()
            if not meta:
                return False, "Meta no encontrada."
            nuevo_monto = float(meta['monto_actual']) + cantidad
            cursor.execute("UPDATE metas_ahorro SET monto_actual = %s WHERE id_meta = %s", (nuevo_monto, id_meta))
            conn.commit()
            if nuevo_monto >= float(meta['monto_objetivo']):
                return True, "🎉 ¡Felicidades! Alcanzaste tu meta de ahorro."
            return True, f"Abono registrado. Llevas ${nuevo_monto:.2f}."
        except Exception as e:
            print(f"Error abonando a meta: {e}")
            return False, "Error al abonar."
        finally:
            conn.close()