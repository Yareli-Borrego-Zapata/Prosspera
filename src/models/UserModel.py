import bcrypt
from .databaseModel import Database

class UsuarioModel:

    def __init__(self):
        self.db = Database()

    def email_existe(self, email):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE email = %s",
            (email,)
        )
        existe = cursor.fetchone() is not None
        conn.close()
        return existe

    def registrar(self, usuario_data):
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(
            usuario_data.password.encode('utf-8'),
            salt
        )
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO usuarios
                (nombre, apellido, email, password, fecha_registro)
                VALUES (%s, %s, %s, %s, NOW())
                """,
                (
                    usuario_data.nombre,
                    usuario_data.apellido,
                    usuario_data.email,
                    hashed_pw.decode('utf-8')
                )
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error en registro: {e}")
            return False
        finally:
            conn.close()

    def validar_login(self, email, password):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM usuarios WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(
            password.encode('utf-8'),
            user['password'].encode('utf-8')
        ):
            return user
        return None

    def obtener_usuario_por_id(self, user_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id_usuario, nombre, apellido, email
            FROM usuarios
            WHERE id_usuario = %s
            """,
            (user_id,)
        )
        usuario = cursor.fetchone()
        conn.close()
        return usuario

    def eliminar_usuario(self, user_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM usuarios WHERE id_usuario = %s",
                (user_id,)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error eliminando usuario: {e}")
            return False
        finally:
            conn.close()

    def actualizar_password_db(self, email, hash_password):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET password = %s WHERE email = %s",
                (hash_password, email)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error actualizando password: {e}")
            return False
        finally:
            conn.close()