from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify







class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'),
        ('OS', 'One Size'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    color = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reorder_level = models.PositiveIntegerField(default=10)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.color}-{self.size}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.color}, {self.get_size_display()})"

    @property
    def stock_status(self):
        if self.quantity == 0:
            return "Out of Stock"
        elif self.quantity <= 5:
            return "Low Stock"
        return "In Stock"

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_wholesale = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({'Wholesale' if self.is_wholesale else 'Retail'})"

class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('CASH', 'Cash'),
        ('CARD', 'Credit Card'),
        ('TRANSFER', 'Bank Transfer'),
    ]

    invoice_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=6, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Invoice #{self.invoice_number} - ${self.total}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} for {self.sale.invoice_number}"

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)