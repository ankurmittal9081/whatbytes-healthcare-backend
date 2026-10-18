from rest_framework import serializers
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            'id',
            'name',
            'specialization',
            'email',
            'phone_number',
            'years_of_experience',
            'hospital_affiliation',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_email(self, value):
        # Email uniqueness check, allowing existing instance during update
        qs = Doctor.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('A doctor with this email already exists.')
        return value.lower()
