from enum import Enum, EnumMeta


class HANDLER:
    # Client
    JOIN_IN = "join_in"
    UPLOAD_DATA = "upload_data"

    # Server
    ASSIGN_ID = "assign_id"

    # Shuffler
    ASSIGN_CLIENTS = 'assign_clients'

    @classmethod
    def register_new_handler(cls, name, value):
        setattr(cls, name, value)

    @classmethod
    def values(cls):
        return [
            v for k, v in cls.__dict__.items()
            if '__' not in k and not isinstance(v, classmethod)
        ]
