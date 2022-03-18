from django.db import models
from andale.utils import unique_slug_generator
from django.conf import settings
from django.urls import reverse

class Product(models.Model):

    CATEGORY_CHOICES = (
        ('comida','Comida'),
        ('bebida','Bebida'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    codigo = models.PositiveIntegerField(null=False, blank=False)
    nombre = models.CharField(max_length=50)
    categoria = models.CharField(max_length=6,choices=CATEGORY_CHOICES, default='comida')
    precio = models.FloatField(blank=False, null=False)
    slug = models.SlugField(max_length=250, unique_for_date='fecha')

    def __str__(self):
        return str(self.nombre)
    
    def save(self, *args, **kwargs):

        self.slug = unique_slug_generator(self, self.nombre, self.slug)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_detail',
                                        args=[self.slug])

    class Meta:
        ordering = ('codigo',)                                            