from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer
from patients.models import Patient
from doctors.serializers import DoctorSerializer

class MappingListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Retrieve all patient-doctor mappings."""
        mappings = PatientDoctorMapping.objects.all().select_related('patient', 'doctor')
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Assign a doctor to a patient."""
        serializer = PatientDoctorMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MappingDetailPatientView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        """
        GET /api/mappings/<patient_id>/
        Get all doctors assigned to a specific patient.
        """
        patient = get_object_or_404(Patient, pk=id)
        mappings = PatientDoctorMapping.objects.filter(patient=patient).select_related('doctor')
        doctors = [m.doctor for m in mappings]
        serializer = DoctorSerializer(doctors, many=True)
        return Response({
            'patient_id': patient.id,
            'patient_name': patient.name,
            'total_doctors': len(doctors),
            'doctors': serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, id):
        """
        DELETE /api/mappings/<id>/
        Remove a doctor from a patient.
        Supports deleting by Mapping ID (primary) or by Patient ID if specified.
        """
        # First attempt: find mapping by primary key
        mapping = PatientDoctorMapping.objects.filter(pk=id).first()
        if mapping:
            mapping.delete()
            return Response({'message': 'Mapping removed successfully.'}, status=status.HTTP_204_NO_CONTENT)

        # Fallback: check if id was passed as patient_id with doctor_id in params/body
        doctor_id = request.data.get('doctor') or request.data.get('doctor_id') or request.query_params.get('doctor_id')
        if doctor_id:
            mapping = PatientDoctorMapping.objects.filter(patient_id=id, doctor_id=doctor_id).first()
            if mapping:
                mapping.delete()
                return Response({'message': 'Mapping removed successfully.'}, status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'detail': f'Mapping with ID {id} not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
