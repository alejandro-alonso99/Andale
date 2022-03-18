from django.db import models
from django.conf import settings
from andale.utils import unique_slug_generator
from django.urls import reverse

class Expense(models.Model):

    TYPE_CHOICES = (
        ('insumos','Insumos'),
        ('servicios','Servicios'),
    )

    fecha = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    monto = models.FloatField()
    tipo = models.CharField(choices=TYPE_CHOICES, max_length=9)
    slug = models.SlugField(max_length=250, unique_for_date=fecha)

    def __str__(self):
        return str(self.nombre) + ' ' + self.fecha.strftime("%d-%m-%Y")
    
    def save(self, *args, **kwargs):

        self.slug = unique_slug_generator(self, self.nombre, self.slug)
        super(Expense, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('expenses:expense_detail',
                                        args=[self.slug])