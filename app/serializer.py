from django.core import serializers
from rest_framework import serializers
from app.models import real_time
from app.models import nasa_data
from app.models import capacity

class RealSerializer(serializers.ModelSerializer):
    class Meta:
        model = real_time
        fields = ['tik','cell_1','cell_2','cell_3','cell_4','cell_5','cell_6','cell_7','cell_8','cell_9','cell_10']
    tik= serializers.CharField(max_length=10)
    cell_1= serializers.FloatField()
    cell_2= serializers.FloatField()
    cell_3= serializers.FloatField()
    cell_4= serializers.FloatField()
    cell_5= serializers.FloatField()
    cell_6= serializers.FloatField()
    cell_7= serializers.FloatField()
    cell_8= serializers.FloatField()
    cell_9= serializers.FloatField()
    cell_10= serializers.FloatField()

class NasaSerializer(serializers.ModelSerializer):
    class Meta:
        model = nasa_data
        fields = ['voltage_measured','current_measured','temperature_measured','current_load',
        'voltage_load','time','capacity','cycle']
    
    voltage_measured=serializers.FloatField()
    current_measured=serializers.FloatField()
    temperature_measured=serializers.FloatField()
    current_load=serializers.FloatField()
    voltage_load=serializers.FloatField()
    time=serializers.FloatField()
    capacity=serializers.FloatField()
    cycle=serializers.IntegerField()

class MySerializer(serializers.ModelSerializer):
    class Meta:
        model = capacity
        fields = ['user_capacity']
    
    user_capacity=serializers.FloatField()