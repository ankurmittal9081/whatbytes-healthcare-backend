from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    # Support both object id and detailed nested representation
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), required=False)

    patient_id = serializers.IntegerField(write_only=True, required=False)
    doctor_id = serializers.IntegerField(write_only=True, required=False)

    patient_details = PatientSerializer(source='patient', read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = (
            'id',
            'patient',
            'doctor',
            'patient_id',
            'doctor_id',
            'patient_details',
            'doctor_details',
            'assigned_date',
            'notes',
        )
        read_only_fields = ('id', 'assigned_date', 'patient_details', 'doctor_details')

    def validate(self, data):
        # Resolve patient
        patient = data.get('patient')
        if not patient and 'patient_id' in data:
            try:
                patient = Patient.objects.get(pk=data['patient_id'])
                data['patient'] = patient
            except Patient.DoesNotExist:
                raise serializers.ValidationError({'patient': 'Patient with this ID does not exist.'})

        # Resolve doctor
        doctor = data.get('doctor')
        if not doctor and 'doctor_id' in data:
            try:
                doctor = Doctor.objects.get(pk=data['doctor_id'])
                data['doctor'] = doctor
            except Doctor.DoesNotExist:
                raise serializers.ValidationError({'doctor': 'Doctor with this ID does not exist.'})

        if not patient or not doctor:
            raise serializers.ValidationError('Both patient and doctor are required.')

        # Check for existing mapping
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError('This doctor is already assigned to this patient.')

        # Remove extra keys before creation
        data.pop('patient_id', None)
        data.pop('doctor_id', None)

        return data
