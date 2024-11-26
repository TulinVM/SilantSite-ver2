from django.contrib import admin

from .models import (
    EquipmentModel,
    EngineModel,
    TransmissionModel,
    DriveAxleModel,
    SteeringAxleModel,
    Client,
    ServiceCompany,
    MaintenanceType,
    FailureNode,
    RecoveryMethod,
    Machine,
    Maintenance,
    Complaint,
    MaintenanceOrganization,
)

# Register your models here.

admin.site.register(EquipmentModel)
admin.site.register(EngineModel)
admin.site.register(TransmissionModel)
admin.site.register(DriveAxleModel)
admin.site.register(SteeringAxleModel)
admin.site.register(Client)
admin.site.register(ServiceCompany)
admin.site.register(MaintenanceType)
admin.site.register(FailureNode)
admin.site.register(RecoveryMethod)
admin.site.register(Machine)
admin.site.register(Maintenance)
admin.site.register(Complaint)
admin.site.register(MaintenanceOrganization)