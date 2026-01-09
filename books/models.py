from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    
    # Validación de ISBN: Solo números y guiones, debe cumplir formato de 10 o 13 dígitos
    isbn = models.CharField(
        max_length=20, 
        unique=True, 
        validators=[
            RegexValidator(
                regex=r'^(?=(?:\D*\d){10}(?:(?:\D*\d){3})?$)[\d-]+$',
                message="El ISBN debe tener 10 o 13 dígitos numéricos."
            )
        ]
    )
    
    # cost_usd debe ser mayor a 0
    cost_usd = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    
    # Este se calculará después, por eso permitimos que sea nulo (null=True)
    selling_price_local = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    # stock_quantity no puede ser negativo
    stock_quantity = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    
    category = models.CharField(max_length=100)
    supplier_country = models.CharField(max_length=50)
    
    # Auditoría: fechas automáticas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title