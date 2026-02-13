from rest_framework import serializers
from .models import Watch

class W_Products(serializers.ModelSerializer):
    class Meta:
        model=Watch
        fields = '__all__'