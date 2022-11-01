from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from main.models import Device, UserDevice, Region, Client
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'client'

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_superuser', )
    list_display_links = ('username', 'first_name', 'last_name', 'is_staff', 'is_superuser', )
    inlines = (ClientInline,)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}), # , 'email'
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'), # , 'groups', 'user_permissions'
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'mac', 'created_at')
    list_display_links = ('name',)
    search_fields = ('name', 'mac',)

admin.site.register(Device, DeviceAdmin)

class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'device_mac', 'device_name', 'created_at')
    list_display_links = ('name',)
    search_fields = ('name', 'device__name', 'device__mac',)

    def device_mac(self, obj):
        link = reverse("admin:main_device_change", args=[obj.device.id])

        return format_html('<a href="{}">{}</a>', link, obj.device.mac)

    def device_name(self, obj):
        link = reverse("admin:main_device_change", args=[obj.device.id])

        return format_html('<a href="{}">{}</a>', link, obj.device.name)

admin.site.register(UserDevice, UserDeviceAdmin)

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)

admin.site.register(Region, RegionAdmin)

#https://stackoverflow.com/questions/2462905/is-it-possible-to-change-the-model-name-in-the-django-admin-site
