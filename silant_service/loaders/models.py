from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

class BaseModel(models.Model):
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class EquipmentModel(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class EngineModel(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class TransmissionModel(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class DriveAxleModel(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class SteeringAxleModel(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Client(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class ServiceCompany(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class MaintenanceType(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class FailureNode(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class RecoveryMethod(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class MaintenanceOrganization(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    

class Machine(models.Model):
    serial_number = models.CharField(max_length=255, verbose_name='Зав. № машины')
    equipment = models.ForeignKey(EquipmentModel, on_delete=models.CASCADE, verbose_name='Модель техники')
    engine_model = models.ForeignKey(EngineModel, on_delete=models.CASCADE, verbose_name='Модель двигателя')
    engine_serial = models.CharField(max_length=255, verbose_name='Зав. № двигателя')
    transmission_model = models.ForeignKey(TransmissionModel, on_delete=models.CASCADE, verbose_name='Модель трансмиссии')
    transmission_serial = models.CharField(max_length=255, verbose_name='Зав. № трансмиссии')
    drive_axle_model = models.ForeignKey(DriveAxleModel, on_delete=models.CASCADE, verbose_name='Модель ведущего моста')
    drive_axle_serial = models.CharField(max_length=255, verbose_name='Зав. № ведущего моста')
    steerable_axle_model = models.ForeignKey(SteeringAxleModel, on_delete=models.CASCADE, verbose_name='Модель управляемого моста')
    steerable_axle_serial = models.CharField(max_length=255, verbose_name='Зав. № управляемого моста')
    delivery_contract = models.CharField(max_length=255, verbose_name='Договор поставки №, дата')
    shipment_date = models.DateField(null=True, verbose_name='Дата отгрузки с завода')
    recipient = models.CharField(max_length=255, verbose_name='Грузополучатель (конечный потребитель)')
    delivery_address = models.CharField(max_length=255, blank=True, verbose_name='Адрес доставки (эксплуатации)')
    configuration = models.CharField(max_length=255, blank=True, verbose_name='Комплектация (доп. опции)')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, verbose_name='Сервисная компания')

    class Meta:
        ordering = ['-shipment_date']

    def __str__(self):
        return f'{self.serial_number} | {self.equipment} | {self.client}'


class Maintenance(models.Model):
    maintenance_type = models.ForeignKey(MaintenanceType, on_delete=models.CASCADE, verbose_name='Вид ТО')
    maintenance_date = models.DateField(null=True, verbose_name='Дата проведения ТО')
    operating_hours = models.IntegerField(verbose_name='Наработка, м/час')
    order_number = models.CharField(max_length=255, verbose_name='№ заказ-наряда')
    order_date = models.DateField(null=True, verbose_name='Дата заказ-наряда')
    maintenance_organization = models.ForeignKey(MaintenanceOrganization, on_delete=models.CASCADE, verbose_name='Организация, проводившая ТО')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name='Машина')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Сервисная компания')

    class Meta:
        ordering = ['-maintenance_date']

    def __str__(self):
        return f"{self.maintenance_type} | {self.machine} | {self.maintenance_date} | {self.machine}"


class Complaint(models.Model):
    failure_date = models.DateField(null=True, verbose_name='Дата отказа')
    operating_hours = models.IntegerField(verbose_name='Наработка, м/час')
    failure_node = models.ForeignKey(FailureNode, on_delete=models.CASCADE, verbose_name='Узел отказа')
    failure_description = models.CharField(max_length=255, verbose_name='Описание отказа')
    recovery_method = models.ForeignKey(RecoveryMethod, on_delete=models.CASCADE, verbose_name='Способ восстановления отказа')
    spare_parts_used = models.CharField(max_length=255, verbose_name='Использованные запчасти')
    recovery_date = models.DateField(null=True, verbose_name='Дата восстановления отказа')
    downtime = models.IntegerField(verbose_name='Время простоя')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name='Машина')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, verbose_name='Сервисная компания')

    class Meta:
        ordering = ['-failure_date']

    def __str__(self):
        return f"{self.failure_node} | {self.recovery_method} | {self.machine}"