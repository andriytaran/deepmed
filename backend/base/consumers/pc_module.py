import json

from channels.generic.websocket import JsonWebsocketConsumer
from pymongo import MongoClient

from base.serializers import ProstateDiagnosisSerializer
from lib.prostate_func import MONGODB_HOST, MONGODB_PORT, COLLECTION_NAME, \
    DBS_NAME, percent_race_by_age, chemo_decisions, radiation_decisions, \
    prostate_cancer_by_size, distribution_by_psa, \
    distribution_by_gleason_pri, distribution_by_gleason_sec, \
    distribution_by_gleason_comb, percent_men_annualy_diagnosed, \
    distribution_by_stage, surgery_decisions


class PCIndividualStatisticsConsumer(JsonWebsocketConsumer):
    serializer_class = ProstateDiagnosisSerializer

    def connect(self):
        # Called on connection. Either call
        if self.scope['user']:
            self.accept()
        else:
            self.close()

    def receive_json(self, content, **kwargs):
        # Remove empty strings
        content = dict((k, v) for k, v in content.items() if v)
        content['user'] = self.scope['user'].id
        serializer = self.serializer_class(data=content)
        if not serializer.is_valid():
            self.send_json({'error': 'Data not valid.',
                            'extra': serializer.errors})
            self.close()

        serializer.save()

        dd = dict(serializer.validated_data)
        dd.pop('user', None)
        dd['gleason-pri'] = dd.pop('gleason_primary', None)
        dd['gleason-sec'] = dd.pop('gleason_secondary', None)

        input_json = json.dumps(dd, ensure_ascii=False)

        mongo_client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        collection = mongo_client[DBS_NAME][COLLECTION_NAME]

        percent_men_annualy_diagnosed_response = \
            percent_men_annualy_diagnosed(input_json, collection)
        self.send_json({'percent_men_annualy_diagnosed':
                            percent_men_annualy_diagnosed_response})

        distribution_by_stage_response = distribution_by_stage(input_json,
                                                               collection)
        self.send_json({'distribution_by_stage':
                            distribution_by_stage_response})

        surgery_decisions_response = surgery_decisions(input_json,
                                                       collection)
        self.send_json({'surgery_decisions': surgery_decisions_response})

        percent_race_by_age_response = percent_race_by_age(input_json,
                                                           collection)
        self.send_json({'percent_race_by_age': percent_race_by_age_response})

        chemo_decisions_response = chemo_decisions(input_json, collection)
        self.send_json({'chemo_decisions': chemo_decisions_response})

        radiation_decisions_response = \
            radiation_decisions(input_json, collection)
        self.send_json({'radiation_decisions': radiation_decisions_response})

        prostate_cancer_by_size_response = \
            prostate_cancer_by_size(input_json, collection)
        self.send_json({'prostate_cancer_by_size':
                            prostate_cancer_by_size_response})

        distribution_by_psa_response = \
            distribution_by_psa(input_json, collection)
        self.send_json({'distribution_by_psa': distribution_by_psa_response})

        distribution_by_gleason_pri_response = \
            distribution_by_gleason_pri(input_json, collection)
        self.send_json({'distribution_by_gleason_pri':
                            distribution_by_gleason_pri_response})

        distribution_by_gleason_sec_response = \
            distribution_by_gleason_sec(input_json, collection)
        self.send_json({'distribution_by_gleason_sec':
                            distribution_by_gleason_sec_response})

        distribution_by_gleason_comb_response = \
            distribution_by_gleason_comb(input_json, collection)
        self.send_json({'distribution_by_gleason_comb':
                            distribution_by_gleason_comb_response})
