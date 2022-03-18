from django.db import models
from django.conf import settings
from andale.utils import unique_slug_generator

class Sale(models.Model):

    ORIGIN_CHOICES = (
        ('mesa','Mesa'),
        ('delivery','Delivery'),
    )

    PAYMENT_CHOICES = (
        ('efectivo','Efectivo'),
        ('tarjeta','Tarjeta'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True),
    origen = models.CharField(choices=ORIGIN_CHOICES),
    total = models.FloatField() 
    slug = models.SlugField(max_length=250,unique_for_date=fecha)

    def __str__(self):
        return  self.fecha.strftime("%d-%m-%Y") + ' ' + str(self.monto)
    
    def save(self, *args, **kwargs):

        self.slug = unique_slug_generator(self, self.id, self.slug)
        super(Sale, self).save(*args, **kwargs)

    '''
    def get_absolute_url(self):
        return reverse('expenses:expense_detail',
                                        args=[self.slug])
    '''