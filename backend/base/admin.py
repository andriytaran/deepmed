from django.contrib import admin
import base.models


@admin.register(base.models.BreastDiagnosisData)
class BreastDiagnosisDataAdmin(admin.ModelAdmin):
    model = base.models.BreastDiagnosisData
    list_per_page = 20
    ordering = ['id']
    search_fields = ['id', 'user__email']
    list_display = ['user_email', 'created_at', 'id']
    readonly_fields = ['id', 'created_at']

    def user_email(self, obj):
        return obj.user.email
