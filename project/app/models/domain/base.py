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
