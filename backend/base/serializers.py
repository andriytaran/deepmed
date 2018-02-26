from rest_framework import serializers

from base.models import BreastDiagnosisData


class CustomAnalyticsSerializer(serializers.Serializer):
    """
    Serializer for custom analytics request input details.
    """
    age = serializers.IntegerField(required=False)
    ethnicity = serializers.CharField(required=False)
    tumor_grade = serializers.FloatField(required=False)
    tumor_size = serializers.CharField(required=False)
    num_pos_nodes = serializers.CharField(required=False)
    er_status = serializers.CharField(required=False)
    pr_status = serializers.CharField(required=False)
    her2_status = serializers.CharField(required=False)
    type = serializers.CharField(required=False)
    tumor_number = serializers.CharField(required=False)
    stage = serializers.CharField(required=False)


class DiagnosisSerializer(serializers.Serializer):
    """
    Serializer for diagnosis request input details.
    """
    age = serializers.IntegerField(required=True)
    tumor_size_in_mm = serializers.IntegerField(required=False, default=0)
    tumor_grade = serializers.FloatField(required=True)
    er_status = serializers.CharField(required=True)
    pr_status = serializers.CharField(required=True)
    her2_status = serializers.CharField(required=True)
    num_pos_nodes = serializers.IntegerField(required=False, default=0)
    ethnicity = serializers.CharField(required=False, default='Caucasian')
    sex = serializers.CharField(required=False, default='Female')
    type = serializers.CharField(required=False, default='IDC')
    site = serializers.CharField(required=False, default='Upper-Outer')
    laterality = serializers.CharField(required=False, default='left')
    stage = serializers.CharField(required=False)
    number_of_tumors = serializers.IntegerField(required=False, default=1)
    region = serializers.CharField(required=False, default='unk')


class DiagnosisDataSerializer(serializers.ModelSerializer):
    sex = serializers.CharField(required=False, default='Female')
    stage_sd = serializers.CharField(
        required=False)  # Replace grouped III stage on original [IIIA, IIIB, IIIC, IIINOS]
    region = serializers.CharField(required=False, default='unk')
    site = serializers.CharField(required=False, default='Upper-Outer')
    ethnicity = serializers.CharField(required=False, default='Caucasian')
    laterality = serializers.CharField(required=False, default='left')
    type = serializers.CharField(required=False, default='IDC')
    number_of_tumors = serializers.IntegerField(required=False, default=1)
    num_pos_nodes = serializers.IntegerField(required=False, default=0)
    tumor_size_in_mm = serializers.IntegerField(required=False, default=0)
    tumor_size_in_mm_sd = serializers.CharField(
        required=False)  # For similar diagnoses function

    class Meta:
        model = BreastDiagnosisData
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}}

    def validate(self, data):
        data = dict(data)
        if data.get('ethnicity') == 'Caucasian':
            data['ethnicity'] = 'White'
        elif data.get('ethnicity') == 'African American':
            data['ethnicity'] = 'Black'
        elif data.get('ethnicity') == 'Asian':
            data['ethnicity'] = 'Asian or Pacific Islander'
        elif data.get('ethnicity') == 'Other':
            data['ethnicity'] = 'Unknown'

        data['tumor_size_in_mm_sd'] = data.get('tumor_size_in_mm', 0)
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

        data['tumor_size'] = data['tumor_size_in_mm']

        if data.get('stage'):
            if data.get('stage') in ['IIIA', 'IIIB', 'IIIC', 'IIINOS']:
                data['stage_sd'] = data.get('stage')
                data['stage'] = 'III'
        else:
            # 0.    1. Any tumor size, dcis or in situ, and No positive nodes
            if data.get('tumor_size_in_mm') in ['<1cm', '<2cm', '<3cm',
                                                '>3cm', '>5cm'] \
                    and data.get('num_pos_nodes') == '0' \
                    and (data.get('type') == 'DCIS'
                         or data.get('region') == 'In Situ'):
                data['stage'] = '0'
            # I.    1. Tumor size <2cm and no positive nodes
            elif data.get('tumor_size_in_mm') == '<2cm' and \
                    data.get('num_pos_nodes') == 0:
                data['stage'] = 'I'
            # IIA.  1. Tumor size <5cm and no positive nodes.
            #       2. Tumor size of <2cm and <3 positive nodes
            elif (data.get('tumor_size_in_mm') in ['<3cm', '>3cm']
                  and data.get('num_pos_nodes') == '0') \
                    or (data.get('tumor_size_in_mm') == '<2cm'
                        and data.get('num_pos_nodes') < 3):
                data['stage'] = 'IIA'
            # IIB.  1. Tumor size <5cm and <3 positive nodes
            #       2. Tumor size >5cm and no positive nodes
            elif (data.get('tumor_size_in_mm') in ['<3cm', '>3cm']
                  and data.get('num_pos_nodes') < 3) \
                    or (data.get('tumor_size_in_mm') == '>5cm'
                        and data.get('num_pos_nodes') == 0):
                data['stage'] = 'IIB'
            # IIIA. 1. Any tumor size and <9 positive nodes
            #       2. Tumor size >5cm and <3 nodes
            elif (data.get('tumor_size_in_mm') in ['<1cm', '<2cm', '<3cm',
                                                   '>3cm', '>5cm']
                  and data.get('num_pos_nodes') < 9) \
                    or (data.get('tumor_size_in_mm') == '>5cm'
                        and data.get('num_pos_nodes') < 3):
                data['stage'] = 'III'
            # IIIB. 1. Any tumor size and IBC and <9 positive nodes
            elif data.get('tumor_size_in_mm') in ['<1cm', '<2cm', '<3cm',
                                                  '>3cm', '>5cm'] \
                    and data.get('type') == 'IBC' \
                    and data.get('num_pos_nodes') < 9:
                data['stage'] = 'III'
            # IIIC. 1. >10 positive nodes and any tumor size
            elif data.get('tumor_size_in_mm') in ['<1cm', '<2cm', '<3cm',
                                                  '>3cm', '>5cm'] \
                    and data.get('num_pos_nodes') > 10:
                data['stage'] = 'III'
            # IV.   1. Regional - Distant
            elif data.get('region') == 'Distant':
                data['stage'] = 'IV'

        if data.get('region', 'unk') == 'unk':
            if data.get('num_pos_nodes', 0) == 0:
                data['region'] = 'Localized'
            elif 0 < data.get('num_pos_nodes', 0) < 9:
                data['region'] = 'Regional'
            elif data.get('num_pos_nodes', 0) >= 9:
                data['region'] = 'Distant'

        if not data.get('stage_sd'):
            data['stage_sd'] = data.get('stage')

        return data

    def create(self, validated_data):
        validated_data['tumor_size_in_mm'] = validated_data.pop(
            'tumor_size_in_mm_sd', None)
        validated_data['stage'] = validated_data.pop('stage_sd', None)
        obj = BreastDiagnosisData.objects.create(**validated_data)
        return obj
