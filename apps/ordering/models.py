from django.db import models
from django.contrib.auth.models import User
from ..products.models import Cart
from ..personal_data.models import UserAddress, UserPymentCard
from django.db.models import Sum

# Create your models here.
class Order(models.Model):
    CHOICES_STATUS = (
        ('Оформлено', 'Оформлено'),
        ('Оплачено', 'Оплачено'),
        ('Отменено', 'Отменено'),
        ('Выполнено', 'Выполнено'),
        ('Не выполнено', 'Не выполнено'),
    )    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    cart = models.ManyToManyField(Cart, related_name='orders')
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    pyment_card = models.ForeignKey(UserPymentCard, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default='Оформлено')
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):  
        return self.user.username
    
