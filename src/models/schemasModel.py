from pydantic import BaseModel, Field, EmailStr, field_validator
import re

class UsuarioSchema(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    apellido: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator('password')
    @classmethod
    def validar_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe tener al menos una letra mayúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('La contraseña debe tener al menos una letra minúscula')
        if not re.search(r'[0-9]', v):
            raise ValueError('La contraseña debe tener al menos un número')
        return v