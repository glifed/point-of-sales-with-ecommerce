from enum import Enum


class APIResponseMessage(str, Enum):
    """User-Friendly API response messages.
    These messages are consumed by front-end,
    for communicating status of the request made
    by the API user.
    """

    # Success messages
    ITEM_DELETED_SUCCESSFULLY = "Elemento eliminado correctamente."

    # Validation messages
    NAME_TAKEN = "Este nombre ya fue tomado."
    INVALID_UUID = "ID de elemento incorrecto."

    # DB messages
    ERROR_IN_SAVING_ITEM = "Error al guardar el ítem. Intente de nuevo."
    ITEM_NOT_FOUND_IN_DB = "Elemento no encontrado en la base de datos."

    # Authentication & Authorization messages
    INVALID_USERNAME_PASSWORD = "Usuario o contraseña incorrecto."
    INACTIVE_USER = "Su usuario está inactivo. Comuníquese con su administrador."
    InsufficientPermissions = (
        "No contiene permisos suficientes para acceder a este recurso."
    )
