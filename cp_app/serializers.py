from rest_framework import serializers
from cp_app.models import Partner

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = (
            'id',
            'user',
            'name',
            'city',
            'address',
            'company_name',
            'cars',
            'created_at',
            'modify_at',
            'deleted_at'
            )