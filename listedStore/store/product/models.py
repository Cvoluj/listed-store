from django.db import models

from store.abstract.models import AbstractModel
from store.user.models import User


class Product(AbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    hidden = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.name    