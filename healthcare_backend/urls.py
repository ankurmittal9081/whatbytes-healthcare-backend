from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'message': 'Welcome to WhatBytes Healthcare Backend API',
        'status': 'operational',
        'version': '1.0.0',
        'endpoints': {
            'authentication': {
                'register': request.build_absolute_uri('/api/auth/register/'),
                'login': request.build_absolute_uri('/api/auth/login/')
            },
            'patients': request.build_absolute_uri('/api/patients/'),
            'doctors': request.build_absolute_uri('/api/doctors/'),
            'mappings': request.build_absolute_uri('/api/mappings/'),
            'admin': request.build_absolute_uri('/admin/')
        },
        'documentation': 'Refer to README.md and postman_collection.json for complete API documentation.'
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/doctors/', include('doctors.urls')),
    path('api/mappings/', include('mappings.urls')),
]
