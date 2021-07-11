from enum import Enum, IntEnum, unique

from tortoise import fields, models


@unique  # avoid duplicate statuses
class Status(IntEnum):
    ACTIVE = 1
    INACTIVE = 0


class StatusMixin:
    status = fields.IntEnumField(Status, default=Status.ACTIVE)


class ItemType(str, Enum):
    PRODUCTO = "producto"
    SERVICIO = "servicio"


class ItemTypeMixin:
    item_type = fields.CharEnumField(ItemType, default=ItemType.PRODUCTO)


class TimestampMixin:
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class NameMixin:
    name = fields.CharField(80)


class AbstractBaseModel(models.Model):
    id = fields.UUIDField(pk=True)

    class Meta:
        abstract = True


class AbstractUserMixin(AbstractBaseModel, TimestampMixin, StatusMixin):
    username = fields.CharField(max_length=50, unique=True, index=True)
    full_name = fields.CharField(max_length=80, index=True)
    hashed_password = fields.CharField(max_length=128, null=False)
    scopes = fields.JSONField(null=True)
    onetime_scopes = fields.JSONField(null=True)
    is_superuser = fields.BooleanField(default=False)

    def __str__(self):
        return f"<User: {self.username}>"

    class Meta:
        abstract = True
