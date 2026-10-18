from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from .models import Doctor

class DoctorTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name='Test Admin',
            email='admin@example.com',
            password='Password123'
        )
        self.client.force_authenticate(user=self.user)
        self.list_create_url = reverse('doctor-list-create')
        self.doctor_data = {
            'name': 'Dr. Sharma',
            'specialization': 'Cardiology',
            'email': 'sharma@hospital.com',
            'phone_number': '9876543210',
            'years_of_experience': 15,
            'hospital_affiliation': 'City General Hospital'
        }

    def test_create_doctor(self):
        response = self.client.post(self.list_create_url, self.doctor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Dr. Sharma')

    def test_list_doctors(self):
        Doctor.objects.create(**self.doctor_data)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_doctor_detail(self):
        doctor = Doctor.objects.create(**self.doctor_data)
        url = reverse('doctor-detail', kwargs={'pk': doctor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['specialization'], 'Cardiology')

    def test_update_doctor(self):
        doctor = Doctor.objects.create(**self.doctor_data)
        url = reverse('doctor-detail', kwargs={'pk': doctor.pk})
        response = self.client.put(url, {'years_of_experience': 16}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        doctor.refresh_from_db()
        self.assertEqual(doctor.years_of_experience, 16)

    def test_delete_doctor(self):
        doctor = Doctor.objects.create(**self.doctor_data)
        url = reverse('doctor-detail', kwargs={'pk': doctor.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Doctor.objects.filter(pk=doctor.pk).exists())
