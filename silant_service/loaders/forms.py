from django import forms
from .models import (
    Maintenance,
    Complaint,
    Machine,
)


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = [
            "maintenance_type",
            "maintenance_date",
            "operating_hours",
            "order_number",
            "order_date",
            "maintenance_organization",
            "machine",
            "service_company",
        ]
        widgets = {
            "maintenance_date": forms.DateInput(attrs={"type": "date"}),
            "order_date": forms.DateInput(attrs={"type": "date"}),
        }


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            "failure_date",
            "operating_hours",
            "failure_node",
            "failure_description",
            "recovery_method",
            "spare_parts_used",
            "recovery_date",
            "downtime",
            "machine",
            "service_company",
        ]
        widgets = {
            "failure_date": forms.DateInput(attrs={"type": "date"}),
            "recovery_date": forms.DateInput(attrs={"type": "date"}),
        }


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = [
            'serial_number',
            'equipment',
            'engine_model',
            'engine_serial',
            'transmission_model',
            'transmission_serial',
            'drive_axle_model',
            'drive_axle_serial',
            'steerable_axle_model',
            'steerable_axle_serial',
            'delivery_contract',
            'shipment_date',
            'recipient',
            'delivery_address',
            'configuration',
            'client',
            'service_company',
        ]
        widgets = {
            'shipment_date': forms.DateInput(attrs={'type': 'date'}),
        }