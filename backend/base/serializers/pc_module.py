from rest_framework import serializers
import base.models


class ProstateDiagnosisSerializer(serializers.ModelSerializer):
    sex = serializers.CharField(required=False, default='Male')

    class Meta:
        model = base.models.ProstateDiagnosisData
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}}

