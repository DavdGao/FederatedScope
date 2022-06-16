
class HANDLER:
    JOIN_IN = "join_in"
    ASSIGN_CLIENT_ID = "assign_client_id"

    @classmethod
    def register_new_handler(cls, name, value):
        setattr(cls, name, value)

