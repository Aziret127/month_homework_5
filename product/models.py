from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
   
class Product(models.Model):
    
    title = models.CharField(max_length=255,)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, )

    def __str__(self):
        return self.title

class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(default=0)
   
    def __str__(self):
        return f"Review for {self.product.title} - {self.stars} stars"

