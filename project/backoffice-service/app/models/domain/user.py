from tortoise import fields

from app.models.domain.base import AbstractUserMixin


class User(AbstractUserMixin):
    cedula = fields.CharField(max_length=11, null=True)
    sueldo = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    comision = fields.FloatField(default=0, null=True)

    class Meta:
        table = "user"
        default_related_name = "users"
        table_description = "App users."
