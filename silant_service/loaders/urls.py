from django.urls import path

from .views import (
    # machine_delete,
    MachineDeleteView,
    MaintenanceDeleteView,
    ComplaintDeleteView,
    unauthorized_index,
    machine_list,
    machine_detail,
    MachineCreateView,
    MachineUpdateView,
    maintenance_list,
    MaintenanceCreateView,
    MaintenanceUpdateView,
    complaint_list,
    ComplaintCreateView,
    ComplaintUpdateView,
)

urlpatterns = [
    path('', unauthorized_index, name='welcome'),
    path('machines/', machine_list, name='machine_list'),
    path('machines/create/', MachineCreateView.as_view(), name='machine_create'),
    path('machines/update/<int:pk>/', MachineUpdateView.as_view(), name='machine_update'),
    # path('machines/delete/<int:machine_id>/', machine_delete, name='machine_delete'),
    path('machines/delete/<int:pk>/', MachineDeleteView.as_view(), name='machine_delete'),  # Удаление машины
    path('machines/<int:machine_id>/', machine_detail, name='machine_detail'),
    
    path('maintenances/', maintenance_list, name='maintenance_list'),
    path('maintenances/create/', MaintenanceCreateView.as_view(), name='maintenance_create'),
    path('maintenances/update/<int:pk>/', MaintenanceUpdateView.as_view(), name='maintenance_update'),
    path('maintenances/delete/<int:pk>/', MaintenanceDeleteView.as_view(), name='maintenance_delete'),
    
    path('complaints/', complaint_list, name='complaints_list'),
    path('complaints/create/', ComplaintCreateView.as_view(), name='complaint_create'),
    path('complaints/update/<int:pk>/', ComplaintUpdateView.as_view(), name='complaint_update'),
    path('complaints/delete/<int:pk>/', ComplaintDeleteView.as_view(), name='complaint_delete'),
]