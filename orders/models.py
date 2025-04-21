from django.db import models

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    model = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_paid = models.DecimalField(max_digits=10, decimal_places=2)
    measure = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.model}"
