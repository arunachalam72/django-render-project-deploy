import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings
# Create your models here.

def validate_phone(value):
    if not value.isdigit() or len(value) < 10:
        raise ValidationError("Phone number must contain at least 10 digits.")

class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile-images/',blank=True, null=True)
    bio = models.TextField(max_length=400,null=True,blank=True)
    phone_number = models.CharField(max_length=15, validators=[validate_phone],blank=True,null=True)

    def __str__(self):
        return self.username


class Catagory(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False,unique=True)
    image=models.ImageField(upload_to='images/catagory/',null=True,blank=True)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text='0-show,1-Hidden')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Catagory,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False,unique=True)
    vendor=models.CharField(max_length=150,null=False,blank=False)
    product_image=models.ImageField(upload_to='images/products/',null=True,blank=True)
    image1 = models.ImageField(upload_to='images/products/', blank=True, null=True)
    image2 = models.ImageField(upload_to='images/products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='images/products/', blank=True, null=True)
    quantity=models.IntegerField(null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    description=models.TextField(max_length=500,null=True,blank=True)
    status=models.BooleanField(default=False,help_text='0-show,1-Hidden')
    trending=models.BooleanField(default=False,help_text='0-default,1-Trending')
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    @property
    def total_price(self):
        return self.quantity * self.product.selling_price

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicates
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} ❤️ {self.product.name}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)

    @property
    def calculated_total(self):
        return sum(item.total_price for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price