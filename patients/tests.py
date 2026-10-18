from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from .models import Patient

class PatientTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name='Doctor User',
            email='doctor@example.com',
            password='Password123'
        )
        self.other_user = User.objects.create_user(
            name='Other User',
            email='other@example.com',
            password='Password123'
        )
        self.list_create_url = reverse('patient-list-create')
        self.client.force_authenticate(user=self.user)

        self.patient_data = {
            'name': 'John Doe',
            'age': 35,
            'gender': 'Male',
            'contact_number': '1234567890',
            'address': '123 Main St',
            'medical_history': 'No allergies'
        }

    def test_unauthenticated_request_fails(self):
        self.client.logout()
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_patient(self):
        response = self.client.post(self.list_create_url, self.patient_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'John Doe')
        self.assertEqual(response.data['created_by'], self.user.id)

    def test_list_patients_only_returns_created_by_user(self):
        # Create one for current user, one for other user
        Patient.objects.create(created_by=self.user, **self.patient_data)
        Patient.objects.create(created_by=self.other_user, name='Jane Doe', age=29, gender='Female', contact_number='9999999999')

        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'John Doe')

    def test_get_patient_detail(self):
        patient = Patient.objects.create(created_by=self.user, **self.patient_data)
        url = reverse('patient-detail', kwargs={'pk': patient.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], patient.name)

    def test_update_patient(self):
        patient = Patient.objects.create(created_by=self.user, **self.patient_data)
        url = reverse('patient-detail', kwargs={'pk': patient.pk})
        response = self.client.put(url, {'name': 'Johnathan Doe'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        patient.refresh_from_db()
        self.assertEqual(patient.name, 'Johnathan Doe')

    def test_delete_patient(self):
        patient = Patient.objects.create(created_by=self.user, **self.patient_data)
        url = reverse('patient-detail', kwargs={'pk': patient.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Patient.objects.filter(pk=patient.pk).exists())
