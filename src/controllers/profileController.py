from models.UserModel import UsuarioModel

class ProfileController:

    def __init__(self):
        self.usuario_model = UsuarioModel()

    def obtener_usuario(self, user_id):

        return self.usuario_model.obtener_usuario_por_id(
            user_id
        )

    def eliminar_cuenta(self, user_id):

        return self.usuario_model.eliminar_usuario(
            user_id
        )