from . import forms
from . import models
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail
import hashlib

def view_logout(request):
    logout(request)

    return redirect('main:homepage')


def view_login(request):
    if request.method == 'POST':
        form = forms.CustomAuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            login(request, user)

            return redirect('main:homepage')
    else:
        form = forms.CustomAuthenticationForm()

    return render(request,
        template_name='main/login.html',
        context={'form': form})


def view_password(request):
    query = request.GET
    userId = query.get('uid', None)

    if userId != None:
        try:
            user = User.objects.get(pk = userId)
            secret = hashlib.md5(user.password.encode()).hexdigest()

            if secret != hashlib.md5(user.password.encode()).hexdigest():
                return HttpResponse('Unauthorized', status=401)

            login(request, user)

            return redirect('main:profile')
        except models.UserDevice.DoesNotExist:
            return HttpResponse('Not found', status=404)

    done = False

    if request.method == 'POST':
        form = forms.CustomPasswordForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')

            try:
                user = User.objects.filter(username=username).first()
                secret = hashlib.md5(user.password.encode()).hexdigest()
                link = 'https://admin.web.one/password?uid=' + str(user.id) + '&secret=' + secret

                send_mail(
                    'web změna hesla',
                    'Pro změnu vašeho hesla použijte tento odkaz: ' + link,
                    'admin@web.one',
                    [user.username],
                    fail_silently=False,
                )
            except Exception:
                pass

            done = True

    form = forms.CustomPasswordForm()

    return render(request,
        template_name='main/password.html',
        context={'form': form, 'done': done})


def view_register(request):
    if request.method == 'POST':
        form_user = forms.CustomUserCreationForm(request.POST)

        if form_user.is_valid():
            form_user.save()
            username = form_user.cleaned_data.get('username')
            password = form_user.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            uTAC = models.UserTermsAndConditions(user=user)
            uTAC.save()

            uc = models.Client(user=user, phone=form_user.cleaned_data.get('client__phone'))
            uc.save()

            login(request, user)

            return redirect('main:homepage')
    else:
        form_user = forms.CustomUserCreationForm()

    return render(request,
        template_name='main/register.html',
        context = {
            'form_user': form_user,
        }
    )


def view_profile(request):
    if not request.user.is_authenticated:
        return redirect('main:login')

    if request.method == 'POST':
        form_profile = forms.CustomUserProfileForm(request.POST, instance=request.user)

        if form_profile.is_valid():
            form_profile.save()

            return redirect('main:profile')
    else:
        form_profile = forms.CustomUserProfileForm(instance=request.user)

    return render(request,
        template_name='main/profile.html',
        context = {
            'form_profile': form_profile,
        }
    )


def view_profile_delete(request):
    if not request.user.is_authenticated:
        return redirect('main:login')

    request.user.delete()

    return redirect('main:homepage')


def view_web(request):
    if not request.user.is_authenticated:
        return redirect('main:login')

    return render(request,
        template_name='main/web.html',
        context={})


def view_web_device(request, userDeviceId):
    try:
        if userDeviceId != 0:
            userDevice = models.UserDevice.objects.get(pk = userDeviceId)
        else:
            device = models.Device(user=request.user)
            userDevice = models.UserDevice(user=request.user, device=device)
    except models.UserDevice.DoesNotExist:
        return HttpResponse('Not found', status=404)

    if not request.user.is_authenticated or (userDevice.user != None and userDevice.user.id != request.user.id):
        return HttpResponse('Unauthorized', status=401)

    device_cron = models.DeviceCron(device=userDevice.device)

    if request.GET.get('user_device', '0') == '1' and request.method == 'POST':
        form_device = forms.CustomUserDeviceForm(request.POST, instance=userDevice)

        if form_device.is_valid():
            userDevice = form_device.save()

            return redirect('main:web_device', userDeviceId=userDevice.id)
    else:
        form_device = forms.CustomUserDeviceForm(instance=userDevice)

    if request.GET.get('device_cron', '0') == '1' and request.method == 'POST':
        form_device_cron = forms.CustomDeviceCronForm(request.POST, instance=device_cron)

        if form_device_cron.is_valid():
            device_cron = form_device_cron.save()

            return redirect('main:web_device', userDeviceId=userDevice.id)
    else:
        form_device_cron = forms.CustomDeviceCronForm(instance=device_cron)

    return render(request,
        template_name='main/web_device.html',
        context = {
            'user_device': userDevice,
            'form_device': form_device,
            'form_device_cron': form_device_cron,
        }
    )


def view_web_device_delete(request, userDeviceId):
    try:
        userDevice = models.UserDevice.objects.get(pk = userDeviceId)
    except models.UserDevice.DoesNotExist:
        return HttpResponse('Not found', status=404)

    if not request.user.is_authenticated or userDevice.user.id != request.user.id:
        return HttpResponse('Unauthorized', status=401)

    if userDevice.device.user != None and userDevice.device.user.id == request.user.id:
        userDevice.device.user = None
        userDevice.device.save()

    userDevice.delete()

    return redirect('main:web')


def view_web_device_cron_delete(request, userDeviceId, deviceCronId):
    try:
        user_device = models.UserDevice.objects.get(pk = userDeviceId)
        device_cron = models.DeviceCron.objects.get(pk = deviceCronId)
    except models.UserDevice.DoesNotExist:
        return HttpResponse('Not found', status=404)

    if not request.user.is_authenticated or user_device.user.id != request.user.id or user_device.device.id != device_cron.device.id:
        return HttpResponse('Unauthorized', status=401)

    device_cron.delete()

    return redirect('main:web_device', userDeviceId=user_device.id)


def view_web_action(request, userDeviceId, action):
    query = request.GET
    deviceId = query.get('device-id', None)
    device = None
    user = None

    if deviceId == None:
        try:
            userDevice = models.UserDevice.objects.get(pk = userDeviceId)
            device = userDevice.device
            user = userDevice.user
        except models.UserDevice.DoesNotExist:
            return HttpResponse('Not found', status=404)

        if not request.user.is_authenticated or userDevice.user.id != request.user.id:
            return HttpResponse('Unauthorized', status=401)
    else:
        if not request.user.is_staff:
            return HttpResponse('Unauthorized', status=401)

        try:
            device = models.Device.objects.get(pk = deviceId)
            user = request.user
        except models.UserDevice.DoesNotExist:
            return HttpResponse('Not found', status=404)

    deviceAction = models.DeviceAction(user=user, device=device, action=action)
    deviceAction.save()

    return HttpResponse('ok')


def view_web_log(request, userDeviceId):
    query = request.GET
    deviceId = query.get('device-id', None)
    rangeFrom = parse_datetime(query.get('from', ''))
    rangeTill = parse_datetime(query.get('till', ''))

    if deviceId == None:
        try:
            userDevice = models.UserDevice.objects.get(pk = userDeviceId)
            device = userDevice.device
        except models.UserDevice.DoesNotExist:
            return HttpResponse('Not found', status=404)
    else:
        try:
            device = models.Device.objects.get(pk = deviceId)
        except models.UserDevice.DoesNotExist:
            return HttpResponse('Not found', status=404)

    if not request.user.is_staff and (not request.user.is_authenticated or userDevice.user.id != request.user.id):
        return HttpResponse('Unauthorized', status=401)

    logResponse = {
        'total_energy': 0,
        'log': [],
    }

#     total_energy = models.DeviceLog.objects.raw("""
#         SELECT t.id, SUM(t.value) r
#         FROM (
#
#         SELECT dl.id, ((AVG(dl.value) * (SELECT value FROM main_devicelog WHERE device_id = dl.device_id AND option = 'voltage' ORDER BY id DESC LIMIT 1) / 1000) * (COUNT(dl.id) * 10 / 3600)) value
#         FROM main_devicelog dl
#         WHERE dl.device_id = '%s' AND dl.option = 'current' AND created_at >= %s AND created_at <= %s
#         GROUP BY dl.device_id
#
#         ) t
#     """, [device.id, rangeFrom, rangeTill])[0].r  # TODO: sec

    total_energy = models.DeviceLog.objects.raw("""
        SELECT t.id, SUM(t.value) r
        FROM (

        SELECT dl.id, ((AVG(dl.value) / 1000) * (COUNT(dl.id) * 10 / 3600)) value
        FROM main_devicelog dl
        WHERE dl.device_id = '%s' AND dl.option = 'apparent' AND created_at >= %s AND created_at <= %s
        GROUP BY dl.device_id

        ) t
    """, [device.id, rangeFrom, rangeTill])[0].r  # TODO: sec

    if total_energy == None:
        total_energy = 0

    logResponse['total_energy'] = total_energy

#     logs = models.DeviceLog.objects.raw("SELECT id, device_id, option, AVG(value) value, MIN(created_at) created_at "
#                                          "FROM main_devicelog "
#                                          "WHERE device_id = '%s' AND option = 'current' AND created_at >= %s AND created_at <= %s"
#                                          "GROUP BY device_id, option, YEAR(created_at), MONTH(created_at), DAY(created_at), HOUR(created_at) "
#                                          "ORDER BY created_at", [device.id, rangeFrom, rangeTill])

    logs = models.DeviceLog.objects.raw("SELECT id, device_id, option, AVG(value) value, MIN(created_at) created_at "
                                         "FROM main_devicelog "
                                         "WHERE device_id = '%s' AND option = 'apparent' AND created_at >= %s AND created_at <= %s"
                                         "GROUP BY device_id, option, YEAR(created_at), MONTH(created_at), DAY(created_at), HOUR(created_at) "
                                         "ORDER BY created_at", [device.id, rangeFrom, rangeTill])

    for log in logs:
        logResponse['log'].append({
            'created_at': log.created_at,
            'option': log.option,
            'value': log.value,
        })

    return JsonResponse(logResponse, safe=False)


def get_regions(calculateEnergy = True):
    regions = []

    for region in models.Region.objects.all():
        current_energy = None
        today_energy = None
        total_energy = None

#         current_energy = models.DeviceLog.objects.raw("""
#             SELECT t.id, SUM(t.value) r
#             FROM (
#
#             SELECT dl.id, (dl.value * (SELECT value FROM main_devicelog WHERE device_id = dl.device_id AND option = 'voltage' ORDER BY id DESC LIMIT 1)) value
#             FROM main_devicelog dl
#             INNER JOIN (SELECT MAX(id) id, device_id FROM main_devicelog WHERE option = 'current' GROUP BY device_id) m ON (m.device_id = dl.device_id AND m.id = dl.id)
#             INNER JOIN main_region_devices rd ON rd.device_id = dl.device_id
#             WHERE rd.region_id = '%s' AND dl.option = 'current'
#             GROUP BY dl.device_id
#
#             ) t
#         """, [region.id])[0].r

#         today_energy = models.DeviceLog.objects.raw("""
#             SELECT t.id, SUM(t.value) r
#             FROM (
#
#             SELECT dl.id, ((AVG(dl.value) * (SELECT value FROM main_devicelog WHERE device_id = dl.device_id AND option = 'voltage' ORDER BY id DESC LIMIT 1) / 1000) * (COUNT(dl.id) * 10 / 3600)) value
#             FROM main_devicelog dl
#             INNER JOIN main_region_devices rd ON rd.device_id = dl.device_id
#             WHERE rd.region_id = '%s' AND dl.option = 'current' AND dl.created_at >= CURDATE()
#             GROUP BY dl.device_id
#
#             ) t
#         """, [region.id])[0].r  # TODO: sec

#         total_energy = models.DeviceLog.objects.raw("""
#             SELECT t.id, SUM(t.value) r
#             FROM (
#
#             SELECT dl.id, ((AVG(dl.value) * (SELECT value FROM main_devicelog WHERE device_id = dl.device_id AND option = 'voltage' ORDER BY id DESC LIMIT 1) / 1000) * (COUNT(dl.id) * 10 / 3600)) value
#             FROM main_devicelog dl
#             INNER JOIN main_region_devices rd ON rd.device_id = dl.device_id
#             WHERE rd.region_id = '%s' AND dl.option = 'current'
#             GROUP BY dl.device_id
#
#             ) t
#         """, [region.id])[0].r  # TODO: sec

        if calculateEnergy == True:
            current_energy = models.DeviceLog.objects.raw("""
                SELECT t.id, SUM(t.value) r
                FROM (

                SELECT dl.id, dl.value
                FROM main_devicelog dl
                INNER JOIN (SELECT MAX(id) id, device_id FROM main_devicelog WHERE option = 'apparent' GROUP BY device_id) m ON (m.device_id = dl.device_id AND m.id = dl.id)
                INNER JOIN main_region_devices rd ON rd.device_id = dl.device_id
                WHERE rd.region_id = '%s' AND dl.option = 'apparent'
                GROUP BY dl.device_id

                ) t
            """, [region.id])[0].r

            today_energy = models.DeviceLog.objects.raw("""
                SELECT t.id, SUM(t.value) r
                FROM (

                SELECT dl.id, ((AVG(dl.value) / 1000) * (COUNT(dl.id) * 10 / 3600)) value
                FROM main_devicelog dl
                INNER JOIN main_region_devices rd ON rd.device_id = dl.device_id
                WHERE rd.region_id = '%s' AND dl.option = 'apparent' AND dl.created_at >= CURDATE()
                GROUP BY dl.device_id

                ) t
            """, [region.id])[0].r  # TODO: sec

            total_energy = models.DeviceLog.objects.raw("""
                SELECT t.id, SUM(t.value) r
                FROM (

                SELECT dl.id, ((AVG(dl.value) / 1000) * (COUNT(dl.id) * 10 / 3600)) value
                FROM main_devicelog dl
                INNER JOIN main_region_devices rd ON rd.device_id = dl.device_id
                WHERE rd.region_id = '%s' AND dl.option = 'apparent'
                GROUP BY dl.device_id

                ) t
            """, [region.id])[0].r  # TODO: sec

#         assert False, locals()

        if current_energy == None:
            current_energy = 0

        if today_energy == None:
            today_energy = 0

        if total_energy == None:
            total_energy = 0

        regions.append({
            'region': region,
            'current_energy': current_energy,
            'today_energy': today_energy,
            'total_energy': total_energy,
        })

    return regions


def view_web_region(request):
    if not request.user.is_authenticated:
        return redirect('main:login')

    if not request.user.is_staff:
        return redirect('main:web')

    return render(request,
        template_name='main/web_region.html',
        context={
            'regions': get_regions(False),
        })


def view_web_region_ajax(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    regionsResponse = []

    for region in get_regions():
        regionsResponse.append({
            'region_id': region['region'].id,
            'current_energy': region['current_energy'],
            'today_energy': region['today_energy'],
            'total_energy': region['total_energy'],
        })

    return JsonResponse(regionsResponse, safe=False)


def view_web_region_detail(request, regionId):
    if not request.user.is_authenticated:
        return redirect('main:login')

    if not request.user.is_staff:
        return redirect('main:web')

    try:
        region = models.Region.objects.get(pk = regionId)
    except models.UserDevice.DoesNotExist:
        return HttpResponse('Not found', status=404)

    return render(request,
        template_name='main/web_region_detail.html',
        context={
            'region': region,
            'regions': get_regions(False),
        })


def view_web_region_log(request, regionId):
    if not request.user.is_authenticated:
        return redirect('main:login')

    if not request.user.is_staff:
        return redirect('main:web')

    try:
        region = models.Region.objects.get(pk = regionId)
    except models.UserDevice.DoesNotExist:
        return HttpResponse('Not found', status=404)

    query = request.GET
    rangeFrom = parse_datetime(query.get('from', ''))
    rangeTill = parse_datetime(query.get('till', ''))

    logResponse = {
        'total_energy': 0,
        'log': [],
    }

    total_energy = models.DeviceLog.objects.raw("""
        SELECT t.id, SUM(t.value) r
        FROM (

        SELECT dl.id, ((AVG(dl.value) / 1000) * (COUNT(dl.id) * 10 / 3600)) value
        FROM main_devicelog dl
        INNER JOIN main_region_devices rd ON (rd.device_id = dl.device_id AND rd.region_id = %s)
        WHERE dl.option = 'apparent' AND created_at >= %s AND created_at <= %s
        GROUP BY rd.region_id

        ) t
    """, [region.id, rangeFrom, rangeTill])[0].r

    if total_energy == None:
        total_energy = 0

    logResponse['total_energy'] = total_energy

    logs = models.DeviceLog.objects.raw("""
        SELECT dl.id, dl.device_id, dl.option, AVG(dl.value) value, MIN(dl.created_at) created_at
        FROM main_devicelog dl
        INNER JOIN main_region_devices rd ON (rd.device_id = dl.device_id AND rd.region_id = %s)
        WHERE dl.option = 'apparent' AND dl.created_at >= %s AND dl.created_at <= %s
        GROUP BY rd.region_id, dl.option, YEAR(dl.created_at), MONTH(dl.created_at), DAY(dl.created_at), HOUR(dl.created_at)
        ORDER BY dl.created_at
    """, [region.id, rangeFrom, rangeTill])

    for log in logs:
        logResponse['log'].append({
            'created_at': log.created_at,
            'option': log.option,
            'value': log.value,
        })

    return JsonResponse(logResponse, safe=False)


def view_homepage(request):
    if request.user.is_authenticated:
        return redirect('main:web')

    return redirect('main:login')

#     return render(request,
#         template_name='main/homepage.html',
#         context={})
