# models.py
from django.db import models
from django.conf import settings
from menu.models import Dish

class orders(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ordered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pickup_time = models.DateTimeField(null=True, blank=True)  # NEW FIELD

    def __str__(self):
        return f"Order #{self.id} - {self.student.username} - {self.dish.name}"
    
    payment_method = models.CharField(
        max_length=10, 
        choices=[('cod', 'Pay at Counter'), ('online', 'Paid Online')],
        default='cod'
    )
