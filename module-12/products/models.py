from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank = True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True) 
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    category = models.ForeignKey(
        Category ,
        on_delete = models.CASCADE,
        related_name = 'products'
     )

    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
  

    def __str__(self):
        return self.name
     