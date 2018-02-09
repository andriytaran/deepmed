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

        # if not data.get('tumor_size') in ['0-2cm', '2-5cm', '5cm+']:
        #     raise ValueError('tumor_size is wrong')
        #
        # if not data.get('num_pos_nodes') in ['0', '1-3', '4-9', '10+']:
        #     raise ValueError('tumor_size is wrong')
        #
        # if not data.get('number_of_tumors') in ['1', '2', '3+']:
        #     raise ValueError('tumor_size is wrong')

        # # 0
        # if data.get('tumor_size') in ['0-2cm', '2-5cm', '5cm+'] and \
        #         data.get('num_pos_nodes') == '0' and data.get('type') in [
        #     'DCIS', 'In Situ']:
        #     data['stage'] = '0'
        # # I
        # elif data.get('tumor_size') == '0-2cm' and \
        #         data.get('num_pos_nodes') == '0':
        #     data['stage'] = 'I'
        # # IIA
        # elif (data.get('tumor_size') == '2-5cm' and \
        #       data.get('num_pos_nodes') == '0') or \
        #         (data.get('tumor_size') == '0-2cm' and \
        #          data.get('num_pos_nodes') == '1-3'):
        #     data['stage'] = 'IIA'
        # # IIB
        # elif (data.get('tumor_size') in ['0-2cm', '2-5cm'] and \
        #       data.get('num_pos_nodes') == '1-3') or \
        #         (data.get('tumor_size') == '5cm+' and \
        #          data.get('num_pos_nodes') == '0'):
        #     data['stage'] = 'IIB'
        # # IIIA
        # elif (data.get('tumor_size') in ['0-2cm', '2-5cm', '5cm+'] and \
        #       data.get('num_pos_nodes') == '4-9') or \
        #         (data.get('tumor_size') == '5cm+' and \
        #          data.get('num_pos_nodes') == '1-3'):
        #     data['stage'] = 'IIIA'
        # # IIIB ????
        # elif (data.get('tumor_size') in ['0-2cm', '2-5cm', '5cm+'] and \
        #       data.get('num_pos_nodes') == '4-9') or \
        #         (data.get('tumor_size') == '5cm+' and \
        #          data.get('num_pos_nodes') == '1-3') or \
        #         data.get('type') == 'IBC':
        #     data['stage'] = 'IIIB'
        # # IIIC
        # elif data.get('num_pos_nodes') == '10+':
        #     data['stage'] = 'IIIC'
        # # IV ???
        # elif data.get('regional') == 'distant':
        #     data['stage'] = 'IV'

        return data
