import smtplib
import secrets
import bcrypt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models.UserModel import UsuarioModel

class AuthController:
    def __init__(self):
        self.usuario_model = UsuarioModel()

    def login(self, email, password, page): 
        try:
            user_db = self.usuario_model.validar_login(email, password)

            if not user_db:
                return None, "Correo o contraseña incorrectos"

            user = {
                "id_usuario": user_db["id_usuario"],
                "nombre": user_db["nombre"],
                "apellido": user_db["apellido"],
                "email": user_db["email"],
                "ultimo_acceso": user_db.get("ultimo_acceso", "Reciente"),
            }

            self.guardar_perfil_en_historial(page, user)

            return user, "Login exitoso"

        except Exception as e:
            return None, f"Error en login: {str(e)}"
    
    def guardar_perfil_en_historial(self, page, user_data):
        """Lógica para recordar la cuenta en el dispositivo"""
        try:
            cuentas = page.client_storage.get("perfiles_activos") or []
            
            nuevo_perfil = {
                "id": user_data['id_usuario'],
                "nombre": user_data['nombre'],
                "email": user_data['email'],
                "fecha": user_data['ultimo_acceso'],
                "foto": user_data.get('foto_perfil', None) 
            }
            
            if not any(p['id'] == nuevo_perfil['id'] for p in cuentas):
                cuentas.append(nuevo_perfil)
        except Exception as e:
            print(f"No se pudo guardar el perfil local: {e}")

    def registrar(self, usuario_data):
        try:
            if self.usuario_model.email_existe(usuario_data.email):
                return False, "El correo electrónico ya está registrado"
            exito = self.usuario_model.registrar(usuario_data)
            
            if exito:
                return True, "Usuario registrado exitosamente"
            else:
                return False, "Error al registrar usuario"
                
        except Exception as e:
            return False, f"Error en registro: {str(e)}"



    def enviar_correo_recuperacion(self, correo_usuario):
        """Verifica existencia del correo y despacha el token por SMTP."""
        try:
            
            if not self.usuario_model.email_existe(correo_usuario):
                print(f"Intento de recuperación fallido: {correo_usuario} no existe.")
                return None

            #
            codigo_verificacion = "".join(secrets.choice("0123456789") for _ in range(6))
            

            remitente = "tu_correo_emisor@gmail.com"
            password_aplicacion = "xxxx xxxx xxxx xxxx" 
            
            msg = MIMEMultipart()
            msg['From'] = remitente
            msg['To'] = correo_usuario
            msg['Subject'] = "Código de Recuperación - Gestor de Finanzas"
            
            cuerpo = (
                f"Hola.\n\n"
                f"Has solicitado restablecer tu acceso. Tu código temporal es:\n\n"
                f"{codigo_verificacion}\n\n"
                f"Si no solicitaste este cambio, puedes ignorar este correo de forma segura."
            )
            msg.attach(MIMEText(cuerpo, 'plain'))
            

            server = smtplib.SMTP('://gmail.com', 587)
            server.starttls()
            server.login(remitente, password_aplicacion)
            server.sendmail(remitente, correo_usuario, msg.as_string())
            server.quit()
            
            return codigo_verificacion  
            
        except Exception as e:
            print(f"Error crítico en el protocolo SMTP: {e}")
            return None

    def actualizar_password(self, correo_usuario, nueva_password):
        """Encripta la nueva clave y hace el llamado de actualización al Modelo."""
        try:

            bytes_password = nueva_password.encode('utf-8')
            sal = bcrypt.gensalt()
            hash_password = bcrypt.hashpw(bytes_password, sal)
            
        
            hash_str = hash_password.decode('utf-8')

            exito = self.usuario_model.actualizar_password_db(correo_usuario, hash_str)
            
            if exito:
                return True, "Contraseña actualizada exitosamente."
            else:
                return False, "No se pudo actualizar la contraseña en el almacenamiento."
                
        except Exception as e:
            print(f"Error de ejecución en actualización backend: {e}")
            return False, f"Error interno: {str(e)}"

def login_exitoso(page, user_data): 
    page.user_data = user_data
    page.go("/dashboard")