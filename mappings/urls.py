from django.urls import path
from .views import MappingListCreateView, MappingDetailPatientView

urlpatterns = [
    path('', MappingListCreateView.as_view(), name='mapping-list-create'),
    path('<int:id>/', MappingDetailPatientView.as_view(), name='mapping-detail-patient'),
]
