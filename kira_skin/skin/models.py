from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class SkinProfile(models.Model):
    SKIN_TYPE_CHOICES = [
        ('dry', 'Dry'),
        ('oily', 'Oily'),
        ('combination', 'Combination'),
        ('hypoallergic', 'Hypoallergic'),
        ('neutral', 'Neutral'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    summer_skin_type = models.CharField(max_length=20, choices=SKIN_TYPE_CHOICES)
    winter_skin_type = models.CharField(max_length=20, choices=SKIN_TYPE_CHOICES)
    spring_skin_type = models.CharField(max_length=20, choices=SKIN_TYPE_CHOICES)
    concerns = models.TextField(blank=True)
    goals = models.TextField(help_text="What are your skincare goals?")
    allergies = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_current_season_skin_type(self):
        current_month = timezone.now().month
        
        # Winter: December (12), January (1), February (2)
        if current_month in [12, 1, 2]:
            return self.winter_skin_type
        # Spring: March (3), April (4), May (5)
        elif current_month in [3, 4, 5]:
            return self.spring_skin_type
        # Summer: June (6), July (7), August (8), September (9), October (10), November (11)
        else:
            return self.summer_skin_type

    def __str__(self):
        return f"{self.user.username}'s Skin Profile"

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('cleanser', 'Cleanser'),
        ('toner', 'Toner'),
        ('serum', 'Serum'),
        ('moisturizer', 'Moisturizer'),
        ('sunscreen', 'Sunscreen'),
        ('mask', 'Face Mask'),
        ('treatment', 'Treatment'),
    ]

    SKIN_TYPE_CHOICES = [
        ('dry', 'Dry'),
        ('oily', 'Oily'),
        ('combination', 'Combination'),
        ('hypoallergic', 'Hypoallergic'),
        ('neutral', 'Neutral'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    suitable_for = models.CharField(max_length=20, choices=SKIN_TYPE_CHOICES, help_text="Suitable skin type")
    ingredients = models.TextField()
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order #{self.order.id}"
