class CRUDBase:
    def __init__(self):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        This object abstracts away the implementation of these methods so that 
        the database ORM is interchangeable and not coupled to the operations.

        **parameters**

        * `model`: An ORM model class
        * `schema`: A Pydantic model (schema) class
        """
        pass

    def get(self):
        pass

    def get_all(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass