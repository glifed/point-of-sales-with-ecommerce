from enum import IntEnum, unique

from tortoise import models, fields


@unique  # avoid duplicate statuses
class Status(IntEnum):
    ACTIVE = 1
    INACTIVE = 0
    DELETED = -1


class StatusMixin():
    status = fields.CharEnumField(Status, default=Status.ACTIVE)


class TimestampMixin():
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class NameMixin():
    name = fields.CharField(80)


class AbstractBaseModel(models.Model):
    id = fields.UUIDField(pk=True)

    class Meta:
        abstract = True
