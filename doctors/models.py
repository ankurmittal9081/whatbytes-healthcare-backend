from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    years_of_experience = models.PositiveIntegerField(default=1)
    hospital_affiliation = models.CharField(max_length=250, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"
