from django.db import models
from account.models import UserAccount
from products.models import Watch

# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(UserAccount,on_delete=models.CASCADE,null=True,blank=True)
    product=models.ForeignKey(Watch,on_delete=models.CASCADE,null=True,blank=True)
    qauntity=models.PositiveIntegerField(default=1)


