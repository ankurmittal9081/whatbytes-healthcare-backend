from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor
from .models import PatientDoctorMapping

class MappingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name='Test User',
            email='user@example.com',
            password='Password123'
        )
        self.client.force_authenticate(user=self.user)

        self.patient = Patient.objects.create(
            name='Patient Alice',
            age=30,
            gender='Female',
            contact_number='1112223333',
            created_by=self.user
        )

        self.doctor = Doctor.objects.create(
            name='Dr. Bob',
            specialization='Neurology',
            email='bob@clinic.com',
            phone_number='4445556666',
            years_of_experience=10
        )

        self.list_create_url = reverse('mapping-list-create')

    def test_assign_doctor_to_patient(self):
        data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'notes': 'Initial consultation'
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['patient'], self.patient.id)
        self.assertEqual(response.data['doctor'], self.doctor.id)

    def test_duplicate_mapping_rejected(self):
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_mappings(self):
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_doctors_for_specific_patient(self):
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        url = reverse('mapping-detail-patient', kwargs={'id': self.patient.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_doctors'], 1)
        self.assertEqual(response.data['doctors'][0]['name'], 'Dr. Bob')

    def test_remove_doctor_from_patient(self):
        mapping = PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        url = reverse('mapping-detail-patient', kwargs={'id': mapping.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PatientDoctorMapping.objects.filter(id=mapping.id).exists())
