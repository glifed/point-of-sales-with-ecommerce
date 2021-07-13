from app.models.domain.base import AbstractBaseModel, NameMixin, TimestampMixin


class Category(AbstractBaseModel, TimestampMixin, NameMixin):
    def __str__(self):
        return f"<Category: {self.name}>"

    class Meta:
        table = "category"
        default_related_name = "categories"
        table_description = "Item categories."
