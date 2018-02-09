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
    ethnicity = serializers.CharField(required=True)
    sex = serializers.CharField(required=False, default='Female')
    type = serializers.CharField(required=False)
    site = serializers.CharField(required=False)
    laterality = serializers.CharField(required=False)
    stage = serializers.CharField(required=False)
    number_of_tumors = serializers.IntegerField(required=True)
    region = serializers.CharField(required=True)


class DiagnosisDataSerializer(serializers.Serializer):
    age = serializers.IntegerField(required=True)
    tumor_size_in_mm = serializers.IntegerField(required=True)
    tumor_grade = serializers.IntegerField(required=True)
    er_status = serializers.CharField(required=True)
    pr_status = serializers.CharField(required=True)
    her2_status = serializers.CharField(required=True)
    num_pos_nodes = serializers.IntegerField(required=True)
    ethnicity = serializers.CharField(required=True)
    sex = serializers.CharField(required=False, default='Female')
    type = serializers.CharField(required=False)
    site = serializers.CharField(required=False)
    laterality = serializers.CharField(required=False)
    stage = serializers.CharField(required=False)
    number_of_tumors = serializers.IntegerField(required=True)
    region = serializers.CharField(required=True)

    def validate(self, data):
        if data.get('ethnicity') == 'Caucasian':
            data['ethnicity'] = 'White'
        elif data.get('ethnicity') == 'African American':
            data['ethnicity'] = 'Black'
        elif data.get('ethnicity') == 'Asian':
            data['ethnicity'] = 'Asian or Pacific Islander'
        elif data.get('ethnicity') == 'Other':
            data['ethnicity'] = 'Unknown'

        # ToDo Ask Nitin about this
        if data.get('tumor_size_in_mm') >= 50:
            data['tumor_size_in_mm'] = ">5cm"
        elif data.get('tumor_size_in_mm') >= 30:
            data['tumor_size_in_mm'] = ">3cm"
        elif data.get('tumor_size_in_mm') >= 20:
            data['tumor_size_in_mm'] = "<3cm"
        elif data.get('tumor_size_in_mm') >= 10:
            data['tumor_size_in_mm'] = "<2cm"
        elif data.get('tumor_size_in_mm') < 10:
            data['tumor_size_in_mm'] = "<1cm"

        return data
