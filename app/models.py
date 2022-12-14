from django.db import models

# Create your models here.
class real_time(models.Model):
    tik= models.CharField(max_length=10, null=True, blank=False)
    cell_1= models.FloatField()
    cell_2= models.FloatField()
    cell_3= models.FloatField()
    cell_4= models.FloatField()
    cell_5= models.FloatField()
    cell_6= models.FloatField()
    cell_7= models.FloatField()
    cell_8= models.FloatField()
    cell_9= models.FloatField()
    cell_10= models.FloatField()

class nasa_data(models.Model):
    voltage_measured=models.FloatField()
    current_measured=models.FloatField()
    temperature_measured=models.FloatField()
    current_load=models.FloatField()
    voltage_load=models.FloatField()
    time=models.FloatField()
    capacity=models.FloatField()
    cycle=models.IntegerField()
class capacity(models.Model):
    user_capacity=models.FloatField()