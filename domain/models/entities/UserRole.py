from enum import Enum


class UserRole(str, Enum):
    administrador = "administrador"
    vendedor = "vendedor"
