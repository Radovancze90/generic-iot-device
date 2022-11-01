import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from django.db.models import Avg, FloatField
from main.models import Device, DeviceLog, UserDevice, Region

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username")


class DeviceLogType(DjangoObjectType):
    class Meta:
        model = DeviceLog
        fields = "__all__" # ("id", "device", "option", "value", "created_at")


class DeviceType(DjangoObjectType):
    class Meta:
        model = Device
        fields = "__all__" # ("id", "mac")

    updated_at = graphene.String()
    relay_state = graphene.String()
    relay_state_updated_at = graphene.String()
    energy_value = graphene.String()
    current_value = graphene.String()
    voltage_value = graphene.String()

    def resolve_updated_at(self, info):
        try:
            last_current = DeviceLog.objects.filter(device__id=self.id, option="current").order_by('-created_at').first()
            return str(last_current.created_at)
        except Exception:
            return None

    def resolve_relay_state(self, info):
        try:
            return str(DeviceLog.objects.filter(device__id=self.id, option="relay").order_by('-created_at').first().value)
        except Exception:
            return "0"

    def resolve_relay_state_updated_at(self, info):
        try:
            last_state = DeviceLog.objects.filter(device__id=self.id, option="relay").order_by('-created_at').first()
            last_other_state = DeviceLog.objects.filter(device__id=self.id, option="relay").exclude(value=last_state.value).order_by('-created_at').first()
            first_same_state = DeviceLog.objects.filter(device__id=self.id, option="relay", value=last_state.value, created_at__gt = last_other_state.created_at).order_by('created_at').first()
            return str(first_same_state.created_at)
        except Exception:
            return None

    def resolve_energy_value(self, info):
        try:
            voltage_value = int(DeviceLog.objects.filter(device__id=self.id, option="voltage").order_by('-created_at').first().value)
            currents_count = DeviceLog.objects.filter(device__id=self.id, option="current").count()
            currents_r = DeviceLog.objects.filter(device__id=self.id, option="current").aggregate(r = Avg('value', output_field=FloatField()))
            energy = (voltage_value * currents_r['r'] / 1000) * (currents_count * 10 / 3600)  # TODO: sec

            return str(energy)
        except Exception:
            return "0"

    def resolve_current_value(self, info):
        try:
            return str(DeviceLog.objects.filter(device__id=self.id, option="current").order_by('-created_at').first().value)
        except Exception:
            return "0"

    def resolve_voltage_value(self, info):
        try:
            return str(DeviceLog.objects.filter(device__id=self.id, option="voltage").order_by('-created_at').first().value)
        except Exception:
            return "240"


class UserDeviceType(DjangoObjectType):
    class Meta:
        model = UserDevice
        fields = "__all__" # ("id", "user", "device", "name", "address_street", "address_city", "address_postal_code", "address_country")


class RegionType(DjangoObjectType):
    class Meta:
        model = Region
        fields = "__all__"


class Query(graphene.ObjectType):
    all_devices = graphene.List(DeviceType)
    all_user_devices = graphene.List(UserDeviceType)
    my_user_devices = graphene.List(UserDeviceType)
    all_regions = graphene.List(RegionType)
    region_by_id = graphene.Field(RegionType, id=graphene.String())

    def resolve_all_devices(root, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return Device.objects.all()
        else:
            return Device.objects.none()

    def resolve_all_user_devices(root, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return UserDevice.objects.all()
        else:
            return UserDevice.objects.none()

    def resolve_my_user_devices(root, info):
        if info.context.user.is_authenticated:
            return UserDevice.objects.filter(user=info.context.user)
        else:
            return UserDevice.objects.none()

    def resolve_all_regions(root, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return Region.objects.all()
        else:
            return Region.objects.none()

    def resolve_region_by_id(root, info, id):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return Region.objects.get(pk=id)
        else:
            return None


schema = graphene.Schema(query=Query)
