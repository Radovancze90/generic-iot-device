from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    outage_notification = models.BooleanField(default=False, blank=False, null=False)

class Device(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, default=None, blank=True, null=True)
    mac = models.CharField(max_length=12)
    model = models.CharField(max_length=100, default=None, null=True)
    brand = models.CharField(max_length=100, default=None, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    outage_report_for = models.DateTimeField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        if self.name:
            return self.name + ' - ' + self.mac

        return self.mac


class DeviceAction(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    finished_at = models.DateTimeField(null=True)

    def __str__(self):
        return "#" + str(self.id) + " - " + self.device.mac


class DeviceLog(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['device', 'option',]),
            models.Index(fields=['device', 'option', 'created_at',]),
        ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    option = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    created_at = models.DateTimeField()

    def __str__(self):
        return "#" + str(self.id) + " - " + self.device.mac


class DeviceCron(models.Model):

    DAY_OF_WEEK_ALL = '0'
    DAY_OF_WEEK_MONDAY = '1'
    DAY_OF_WEEK_TUESDAY = '2'
    DAY_OF_WEEK_WEDNESDAY = '3'
    DAY_OF_WEEK_THURSDAY = '4'
    DAY_OF_WEEK_FRIDAY = '5'
    DAY_OF_WEEK_SATURDAY = '6'
    DAY_OF_WEEK_SUNDAY = '7'
    DAY_OF_WEEK_CHOICES = (
        (DAY_OF_WEEK_ALL, 'Nerozhoduje'),
        (DAY_OF_WEEK_MONDAY, 'Pondělí'),
        (DAY_OF_WEEK_TUESDAY, 'Úterý'),
        (DAY_OF_WEEK_WEDNESDAY, 'Středa'),
        (DAY_OF_WEEK_THURSDAY, 'Čtvrtek'),
        (DAY_OF_WEEK_FRIDAY, 'Pátek'),
        (DAY_OF_WEEK_SATURDAY, 'Sobota'),
        (DAY_OF_WEEK_SUNDAY, 'Neděle'),
    )

    DAY_OF_MONTH_CHOICES = (
        ('0', 'Nerozhoduje'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
    )

    HOUR_CHOICES = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
    )

    MINUTE_CHOICES = (
        ('0', '0'),
#         ('1', '1'),
#         ('2', '2'),
#         ('3', '3'),
#         ('4', '4'),
#         ('5', '5'),
#         ('6', '6'),
#         ('7', '7'),
#         ('8', '8'),
#         ('9', '9'),
#         ('10', '10'),
#         ('11', '11'),
#         ('12', '12'),
#         ('13', '13'),
#         ('14', '14'),
#         ('15', '15'),
#         ('16', '16'),
#         ('17', '17'),
#         ('18', '18'),
#         ('19', '19'),
#         ('20', '20'),
#         ('21', '21'),
#         ('22', '22'),
#         ('23', '23'),
#         ('24', '24'),
#         ('25', '25'),
#         ('26', '26'),
#         ('27', '27'),
#         ('28', '28'),
#         ('29', '29'),
        ('30', '30'),
#         ('31', '31'),
#         ('32', '32'),
#         ('33', '33'),
#         ('34', '34'),
#         ('35', '35'),
#         ('36', '36'),
#         ('37', '37'),
#         ('38', '38'),
#         ('39', '39'),
#         ('40', '40'),
#         ('41', '41'),
#         ('42', '42'),
#         ('43', '43'),
#         ('44', '44'),
#         ('45', '45'),
#         ('46', '46'),
#         ('47', '47'),
#         ('48', '48'),
#         ('49', '49'),
#         ('50', '50'),
#         ('51', '51'),
#         ('52', '52'),
#         ('53', '53'),
#         ('54', '54'),
#         ('55', '55'),
#         ('56', '56'),
#         ('57', '57'),
#         ('58', '58'),
#         ('59', '59'),
    )

    ACTION_ON = 'relay_on'
    ACTION_OFF = 'relay_off'
    ACTION_CHOICES = (
        (ACTION_ON, 'Zapnout'),
        (ACTION_OFF, 'Vypnout'),
    )

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=100, choices=DAY_OF_WEEK_CHOICES, default=DAY_OF_WEEK_ALL)
    day_of_month = models.CharField(max_length=100, choices=DAY_OF_MONTH_CHOICES, default='0')
    hour = models.CharField(max_length=100, choices=DAY_OF_MONTH_CHOICES, default='0')
    minute = models.CharField(max_length=100, choices=DAY_OF_MONTH_CHOICES, default='0')
    action = models.CharField(max_length=100, choices=ACTION_CHOICES, default=ACTION_ON)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

#     def get_day_of_week(self):
#         for e in self.DAY_OF_WEEK_CHOICES:
#             if e[0] == self.day_of_week:
#                 return e[1]
#
#         return self.day_of_week
#
#     def get_day_of_month(self):
#         for e in self.DAY_OF_MONTH_CHOICES:
#             if e[0] == self.day_of_month:
#                 return e[1]
#
#         return self.day_of_month

    def get_action(self):
        for e in self.ACTION_CHOICES:
            if e[0] == self.action:
                return e[1]

        return self.action

    def __str__(self):
        return "#" + str(self.id) + " - " + self.device.mac


class UserDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address_street = models.CharField(max_length=100, default=None, blank=True, null=True)
    address_city = models.CharField(max_length=100, default=None, blank=True, null=True)
    address_postal_code = models.CharField(max_length=100, default=None, blank=True, null=True)
    address_country = models.CharField(max_length=100, default=None, blank=True, null=True)
    outage_notification = models.BooleanField(default=True, blank=False, null=False)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.user.username) + " - " + self.device.mac


class UserTermsAndConditions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.user.username) + " - " + str(self.created_at)

class Region(models.Model):
    devices = models.ManyToManyField(Device)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name

# class RegionDevice(models.Model):
#     region = models.ForeignKey(Device, on_delete=models.CASCADE)
#     device = models.ForeignKey(Device, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(default=datetime.now, blank=True)
#
#     def __str__(self):
#         return self.name
