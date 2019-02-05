from django.db import models

# Create your models here.
class Basic_Model(models.Model):
    appliance_type      = models.CharField(max_length=35)
    store_name          = models.CharField(max_length=35)
    start_url           = models.CharField(max_length=150)


class Appliance_Model(models.Model):
    basic_model         = models.ForeignKey('Basic_Model', on_delete=models.CASCADE)
    short_description   = models.CharField(max_length=300)
    manufacturer        = models.CharField(max_length=1500)
    color               = models.CharField(max_length=20)
    model_number        = models.CharField(max_length=20)
    sku                 = models.CharField(max_length=20)
    full_price          = models.DecimalField(max_digits=7, decimal_places=2)
    sale_price          = models.DecimalField(max_digits=7, decimal_places=2)
    open_box_price      = models.DecimalField(max_digits=7, decimal_places=2)
    img_url             = models.CharField(max_length=150)


class OpenBox_Model(models.Model):
    appliance_type      = models.ForeignKey('Appliance_Model', on_delete=models.CASCADE)
    condition           = models.CharField(max_length=30)
    open_price          = models.DecimalField(max_digits=7, decimal_places=2)
    availability        = models.CharField(max_length=30)


class Appliance_Filter_Model(models.Model):
    manufacturer_sort   = models.CharField(max_length=300, null=True, blank=True)
    price_sort          = models.CharField(max_length=300, null=True, blank=True)
