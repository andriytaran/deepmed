from django.db import models


class BreastDiagnosisData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('accounts.User', related_name='breast_diagnoses',
                             on_delete=models.SET_NULL, null=True)
    age = models.IntegerField(default=18, blank=False, null=False)
    tumor_size_in_mm = models.IntegerField(blank=False, null=False)
    tumor_grade = models.IntegerField(blank=False, null=False)
    er_status = models.CharField(max_length=64, blank=False, null=False)
    pr_status = models.CharField(max_length=64, blank=False, null=False)
    her2_status = models.CharField(max_length=64, blank=False, null=False)
    num_pos_nodes = models.IntegerField(default=0, blank=False, null=False)
    ethnicity = models.CharField(max_length=64, blank=False, null=False)
    sex = models.CharField(max_length=64, blank=False, null=False,
                           default='Female')
    type = models.CharField(max_length=64, blank=False, null=False)
    site = models.CharField(max_length=64, blank=True, null=True)
    laterality = models.CharField(max_length=64, blank=False, null=False)
    stage = models.CharField(max_length=64, blank=True, null=True)
    number_of_tumors = models.IntegerField(blank=True, null=True, default=0)
    region = models.CharField(max_length=64, blank=True, null=True,
                              default='unk')
