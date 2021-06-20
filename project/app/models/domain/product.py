from project.app.models.domain.base import (
    AbstractBaseModel,
    NameMixin,
    StatusMixin,
    TimestampMixin,
    ItemTypeMixin
)
from tortoise import fields

from app.models.domain.base import *

class Product(AbstractBaseModel, NameMixin, TimestampMixin, StatusMixin, ItemTypeMixin):
    sku = fields.CharField(max_length=20, index=True, null=True)
    serial_number = fields.CharField(max_length=20, index=True, null=True)
    description = fields.TextField(null=True)
    images = fields.JSONField(null=True)
    qty = fields.IntField(default=0)
    min_qty = fields.IntField(default=5)
    cost = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    margin = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    rating = fields.IntField(default=5)
    excento_itbis = fields.BooleanField(default=False)
    
# TODO