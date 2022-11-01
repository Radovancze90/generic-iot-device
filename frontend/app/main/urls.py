from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('logout/', views.view_logout, name='logout'),
    path('login/', views.view_login, name='login'),
    path('password/', views.view_password, name='password'),
    path('register/', views.view_register, name='register'),
    path('profile/', views.view_profile, name='profile'),
    path('profile/delete/', views.view_profile_delete, name='profile_delete'),
    path('web/', views.view_web, name='web'),
    path('web/<int:userDeviceId>/', views.view_web_device, name='web_device'),
    path('web/<int:userDeviceId>/delete/', views.view_web_device_delete, name='web_device_delete'),
    path('web/<int:userDeviceId>/cron/<int:deviceCronId>/delete/', views.view_web_device_cron_delete, name='web_device_cron_delete'),
    path('web/<int:userDeviceId>/action/<slug:action>/', views.view_web_action, name='web_action'),
    path('web/<int:userDeviceId>/log/', views.view_web_log, name='web_log'),
    path('web-region/', views.view_web_region, name='web_region'),
    path('web-region.json', views.view_web_region_ajax, name='web_region_ajax'),
    path('web-region/<int:regionId>', views.view_web_region_detail, name='web_region_detail'),
    path('web-region/<int:regionId>/log/', views.view_web_region_log, name='web_region_log'),
    path('', views.view_homepage, name='homepage'),
]
