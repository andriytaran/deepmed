from rest_framework import serializers


class DiagnosisSerializer(serializers.Serializer):
    """
    Serializer for diagnosis request input details.
    """
    age = serializers.IntegerField(required=True)
    tumor_grade = serializers.IntegerField(required=True)
    er_status = serializers.CharField(required=True)
    pr_status = serializers.CharField(required=True)
    tumor_size_in_mm = serializers.IntegerField(required=True)
    num_pos_nodes = serializers.IntegerField(required=True)
    her2_status = serializers.CharField(required=True)
    ethnicity = serializers.CharField(required=False)
