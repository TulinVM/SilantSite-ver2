from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseNotAllowed

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import DeleteView, CreateView, UpdateView



from .models import (
    Machine,
    Client,
    Maintenance,
    EquipmentModel,
    EngineModel,
    TransmissionModel,
    DriveAxleModel,
    SteeringAxleModel,
    ServiceCompany,
    MaintenanceType,
    FailureNode,
    RecoveryMethod,
    Complaint,
    MaintenanceOrganization,          
)

from .forms import (
    MaintenanceForm,
    ComplaintForm,
    MachineForm,
)


from .filters import (
    MachineFilter,
    MaintenanceFilter,
    ComplaintFilter,
)

# Create your views here.


def unauthorized_index(request):
    if request.user.is_authenticated:
        return redirect("machine_list")

    if request.method == "POST":
        serial_number = request.POST.get("serial_number")
        machine = (
            Machine.objects.filter(serial_number=serial_number)
            .values(
                "serial_number",
                "equipment",
                "engine_model",
                "engine_serial",
                "transmission_model",
                "transmission_serial",
                "drive_axle_model",
                "drive_axle_serial",
                "steerable_axle_model",
                "steerable_axle_serial",
            )
            .first()
        )
# 
        model_of_equipment_name = (
            EquipmentModel.objects.filter(id=machine["equipment"])
            .values("id", "name")
            .first()
        )

        model_of_engine_name = (
            EngineModel.objects.filter(id=machine["engine_model"])
            .values("id", "name")
            .first()
        )

        model_of_transmission_name = (
            TransmissionModel.objects.filter(id=machine["transmission_model"])
            .values("id", "name")
            .first()
        )

        model_of_drive_axle_name = (
            DriveAxleModel.objects.filter(id=machine["drive_axle_model"])
            .values("id", "name")
            .first()
        )

        model_of_steerable_axle_model = (
            SteeringAxleModel.objects.filter(id=machine["steerable_axle_model"])
            .values("id", "name")
            .first()
        )
# 
        if (
            machine
            and model_of_equipment_name
            and model_of_engine_name
            and model_of_transmission_name
            and model_of_drive_axle_name
            and model_of_steerable_axle_model
        ):
            return render(
                request,
                "main/index.html",
                {
                    "machine": machine,
                    "model_of_equipment_name": model_of_equipment_name["name"],
                    "model_of_equipment_id": model_of_equipment_name["id"],
                    "model_of_engine_name": model_of_engine_name["name"],
                    "model_of_engine_id": model_of_engine_name["id"],
                    "model_of_transmission_name": model_of_transmission_name["name"],
                    "model_of_transmission_id": model_of_transmission_name["id"],
                    "model_of_drive_axle_name": model_of_drive_axle_name["name"],
                    "model_of_drive_axle_id": model_of_drive_axle_name["id"],
                    "model_of_steering_axle_name": model_of_steerable_axle_model["name"],
                    "model_of_steering_axle_id": model_of_steerable_axle_model["id"],
                },
            )
        else:
            return render(request, "main/index.html", {"error_message": "Not found"})
    return render(request, "main/index.html")


@login_required
@permission_required("loaders.view_machine", raise_exception=True)
def machine_list(request):
    user_id = request.user.id
    can_add_machine = request.user.has_perm("loaders.add_machine")
    can_update_machine = request.user.has_perm("loaders.change_machine")
    can_delete_machine = request.user.has_perm("loaders.delete_machine")
    client = None
    username = request.user.first_name

    try:
        client = Client.objects.get(user_id=user_id)
    except Client.DoesNotExist:
        try:
            service_company = ServiceCompany.objects.get(user_id=user_id)
        except ServiceCompany.DoesNotExist:
            client = username         
            machines = Machine.objects.all().order_by('serial_number')
            machine_filter = MachineFilter(request.GET, queryset=machines)

            return render(
                request,
                "machine/machine_list.html",
                {
                    "machines": machines,
                    "filter": machine_filter,
                    "can_add_machine": can_add_machine,
                    "can_update_machine": can_update_machine,
                    "can_delete_machine": can_delete_machine,
                    "client": client,
                    "username": username,
                },
            )
        client = username
        machines = Machine.objects.filter(service_company_id=service_company.id)
        machine_filter = MachineFilter(request.GET, queryset=machines)

        return render(
            request,
            "machine/machine_list.html",
            {
                "machines": machines,
                "filter": machine_filter,
                "can_add_machine": can_add_machine,
                "can_update_machine": can_update_machine,
                "can_delete_machine": can_delete_machine,
                "client": client,
                "username": username,
            },
        )

    machines = Machine.objects.filter(client=client).order_by('serial_number')
    machine_filter = MachineFilter(request.GET, queryset=machines)

    return render(
        request,
        "machine/machine_list.html",
        {
            "machines": machines,
            "client": client,
            "filter": machine_filter,
            "can_add_machine": can_add_machine,
            "can_update_machine": can_update_machine,
            "can_delete_machine": can_delete_machine,
        },
    )


class MachineDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Machine
    template_name = 'machine/machine_delete.html'  # Шаблон для подтверждения удаления
    success_url = reverse_lazy('machine_list')  # URL, на который произойдет перенаправление после удаления
    permission_required = 'loaders.delete_machine'



class MaintenanceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Maintenance
    template_name = 'maintenance/maintenance_delete.html'  # Шаблон для подтверждения удаления
    success_url = reverse_lazy('maintenance_list')  # URL, на который произойдет перенаправление после удаления
    permission_required = 'loaders.delete_machine'



@login_required
@permission_required("loaders.view_machine", raise_exception=True)
@permission_required("loaders.view_maintenance", raise_exception=True)
def machine_detail(request, machine_id):
    client = None
    username = request.user.first_name

    try:
        machine = Machine.objects.get(id=machine_id)
    except Machine.DoesNotExist:
        return redirect("machine_list")

    try:
        client = Client.objects.get(user_id=request.user.id)
    except Client.DoesNotExist:
        client = username

    maintenances = Maintenance.objects.filter(machine_id=machine_id)
    maintenances_filter = MaintenanceFilter(request.GET, queryset=maintenances)

    return render(
        request,
        "machine/machine_detail.html",
        {
            "machine": machine,
            "maintenances": maintenances,
            "username": username,
            "client": client,
            "filter": maintenances_filter,
        },
    )


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("loaders.add_machine", raise_exception=True), name="dispatch"
)
class MachineCreateView(CreateView):
    form_class = MachineForm
    model = Machine
    template_name = "machine/machine_create.html"
    success_url = "/machines/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.user.first_name
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("loaders.change_machine", raise_exception=True), name="dispatch"
)
class MachineUpdateView(UpdateView):
    form_class = MachineForm
    model = Machine
    template_name = "machine/machine_create.html"
    success_url = "/machines/"


@login_required
@permission_required("loaders.view_maintenance", raise_exception=True)
def maintenance_list(request):
    client = None
    username = request.user.first_name
    service_company = None

    can_add_maintenances = request.user.has_perm("loaders.add_maintenance")
    can_update_maintenance = request.user.has_perm("loaders.change_maintenance")
    can_delete_maintenance = request.user.has_perm("loaders.delete_maintenance")

    try:
        client = Client.objects.get(user_id=request.user.id)
    except Client.DoesNotExist:
        try:
            service_company = ServiceCompany.objects.get(user_id=request.user.id)
        except ServiceCompany.DoesNotExist:
            maintenances = Maintenance.objects.all().order_by('machine__serial_number')
            maintenances_filter = MaintenanceFilter(request.GET, queryset=maintenances)

            return render(
                request,
                "maintenance/maintenance_list.html",
                {
                    "maintenances": maintenances,
                    "filter": maintenances_filter,
                    "can_add_maintenance": can_add_maintenances,
                    "can_update_maintenance": can_update_maintenance,
                    "can_delete_maintenance": can_delete_maintenance,
                    "username": username,
                    "client": client,
                },
            )

        client = username
        maintenances = Maintenance.objects.filter(service_company_id=service_company.id)
        maintenances_filter = MaintenanceFilter(request.GET, queryset=maintenances)

        return render(
            request,
            "maintenance/maintenance_list.html",
            {
                "maintenances": maintenances,
                "filter": maintenances_filter,
                "can_add_maintenance": can_add_maintenances,
                "can_update_maintenance": can_update_maintenance,
                "can_delete_maintenance": can_delete_maintenance,
                "username": username,
                "client": client,
            },
        )
    client_machines = Machine.objects.filter(client=client).order_by('serial_number')
    maintenances = Maintenance.objects.filter(machine__in=client_machines)
    maintenances_filter = MaintenanceFilter(request.GET, queryset=maintenances)

    return render(
        request,
        "maintenance/maintenance_list.html",
        {
            "maintenances": maintenances,
            "client": client,
            "filter": maintenances_filter,
            "can_add_maintenance": can_add_maintenances,
            "can_update_maintenance": can_update_maintenance,
            "can_delete_maintenance": can_delete_maintenance,
        },
    )


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("loaders.add_maintenance", raise_exception=True), name="dispatch"
)
class MaintenanceCreateView(CreateView):
    form_class = MaintenanceForm
    model = Maintenance
    template_name = "maintenance/maintenance_create.html"
    success_url = "/maintenances/"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        try:
            client = Client.objects.get(user=self.request.user)

            form.fields["machine"].queryset = Machine.objects.filter(client=client)
        except Client.DoesNotExist:
            pass

        try:
            service_company = ServiceCompany.objects.get(user=self.request.user)
            form.fields["service_company"].queryset = ServiceCompany.objects.filter(id=service_company.id)
        except ServiceCompany.DoesNotExist:
            pass

        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.user.first_name
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("loaders.change_maintenance", raise_exception=True),
    name="dispatch",
)
class MaintenanceUpdateView(UpdateView):
    form_class = MaintenanceForm
    model = Maintenance
    template_name = "maintenance/maintenance_create.html"
    success_url = "/maintenances/"


@login_required
@permission_required("loaders.view_complaint", raise_exception=True)
def complaint_list(request):
    can_add_complaints = request.user.has_perm("loaders.add_complaint")
    can_update_complaints = request.user.has_perm("loaders.change_complaint")
    can_delete_complaints = request.user.has_perm("loaders.delete_complaint")
    client = None
    username = request.user.first_name

    try:
        client = Client.objects.get(user_id=request.user.id)
    except Client.DoesNotExist:
        try: 
            service_company = ServiceCompany.objects.get(user_id=request.user.id)
        except ServiceCompany.DoesNotExist:
            complaints = Complaint.objects.all().order_by('machine__serial_number')
            complaints_filter = ComplaintFilter(request.GET, queryset=complaints)

            return render(
                request,
                "complaints/complaints_list.html",
                {
                    "complaints": complaints,
                    "filter": complaints_filter,
                    "can_add_complaint": can_add_complaints,
                    "can_update_complaint": can_update_complaints,
                    "can_delete_complaint": can_delete_complaints,
                    "username": username,
                    "client": client,
                },
            )
        
        client = username
        complaints = Complaint.objects.filter(service_company_id=service_company.id).order_by('machine__serial_number')
        complaints_filter = ComplaintFilter(request.GET, queryset=complaints)

        return render(
            request,
            "complaints/complaints_list.html",
            {
                "complaints": complaints,
                "filter": complaints_filter,
                "can_add_complaint": can_add_complaints,
                "can_update_complaint": can_update_complaints,
                "can_delete_complaint": can_delete_complaints,
                "username": username,
                "client": client,
            },
        )
    client_machines = Machine.objects.filter(client=client)
    complaints = Complaint.objects.filter(machine__in=client_machines)
    complaints_filter = ComplaintFilter(request.GET, queryset=complaints)

    return render(
        request,
        "complaints/complaints_list.html",
        {
            "complaints": complaints,
            "client": client,
            "filter": complaints_filter,
            "can_add_complaint": can_add_complaints,
            "can_update_complaint": can_update_complaints,
            "can_delete_complaint": can_delete_complaints,
        },
    )


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("loaders.add_complaint", raise_exception=True), name="dispatch"
)
class ComplaintCreateView(CreateView):
    form_class = ComplaintForm
    model = Complaint
    template_name = "complaints/complaint_create.html"
    success_url = "/complaints/"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        try:
            service_company = ServiceCompany.objects.get(user=self.request.user)
            form.fields["service_company"].queryset = ServiceCompany.objects.filter(id=service_company.id)
        except ServiceCompany.DoesNotExist:
            pass

        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.user.first_name
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("loaders.change_complaint", raise_exception=True),
    name="dispatch",
)
class ComplaintUpdateView(UpdateView):
    form_class = ComplaintForm
    model = Complaint
    template_name = "complaints/complaint_create.html"
    success_url = "/complaints/"


from .models import Machine, Maintenance, Complaint

class ComplaintDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Complaint
    template_name = 'complaints/complaint_delete.html'  # Шаблон для подтверждения удаления
    success_url = reverse_lazy('complaint_list')  # URL, на который произойдет перенаправление после удаления
    permission_required = 'loaders.delete_machine'
