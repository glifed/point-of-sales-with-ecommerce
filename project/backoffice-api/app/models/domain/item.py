from tortoise import fields

from app.models.domain.base import (
    AbstractBaseModel,
    ItemTypeMixin,
    NameMixin,
    StatusMixin,
    TimestampMixin,
)


class Item(AbstractBaseModel, NameMixin, TimestampMixin, StatusMixin, ItemTypeMixin):
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

    def __str__(self):
        return f"<Item: {self.name}>"

    class Meta:
        table = "item"
        default_related_name = "items"
        table_description = "Items, represents products or services"


# TODO
