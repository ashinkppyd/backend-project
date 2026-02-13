from django.db import models
from account.models import UserAccount
from products.models import Watch


class Order(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Watch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()


