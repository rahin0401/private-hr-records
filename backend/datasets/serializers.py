from rest_framework import serializers
from .models import DatasetField



class DatasetFieldSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DatasetField
        fields =["id","field_name","field_type","created_at"]
        read_only_fields =["id","created_at"]
