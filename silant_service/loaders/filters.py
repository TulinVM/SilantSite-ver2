import django_filters

from .models import (
    Machine,
    Maintenance,
    Complaint,
)

class MachineFilter(django_filters.FilterSet):
    class Meta:
        model = Machine
        fields = [
            'equipment', 
            'engine_model',
            'transmission_model',
            'drive_axle_model',
            'steerable_axle_model',
            'serial_number',
        ]

class MaintenanceFilter(django_filters.FilterSet):
    serial_number = django_filters.CharFilter(field_name='machine__serial_number')
    class Meta:
        model = Maintenance
        fields = [
            'maintenance_type',
            'service_company',
            'serial_number',
        ]


class ComplaintFilter(django_filters.FilterSet):
    serial_number = django_filters.CharFilter(field_name='machine__serial_number')
    class Meta:
        model = Complaint
        fields = [
            'failure_node',
            'recovery_method',
            'service_company',
            'serial_number',
        ]