from rest_framework import serializers


class DiagnosisSerializer(serializers.Serializer):
    """
    Serializer for diagnosis request input details.
    """
    age = serializers.IntegerField(required=True)
    tumor_size_in_mm = serializers.IntegerField(required=True)
    tumor_grade = serializers.IntegerField(required=True)
    er_status = serializers.CharField(required=True)
    pr_status = serializers.CharField(required=True)
    her2_status = serializers.CharField(required=True)
    num_pos_nodes = serializers.IntegerField(required=True)
    ethnicity = serializers.CharField(required=False)
    sex = serializers.CharField(required=False, default='Female')
    type = serializers.CharField(required=False)
    site = serializers.CharField(required=False)
    laterality = serializers.CharField(required=False)
    stage = serializers.CharField(required=False)
