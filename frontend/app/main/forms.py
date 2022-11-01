from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from . import models

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(max_length = 100, required = True, label = 'Email', widget = forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length = 100, required = True, label = 'Heslo', widget = forms.PasswordInput(attrs={'placeholder': 'Heslo'}))
    remember_me = forms.BooleanField(required = False, label = 'Zůstat přihlášen')

    class Meta:
        model = User
        fields = ['username', 'password']

class CustomPasswordForm(forms.Form):
    username = forms.EmailField(max_length = 100, required = True, label = 'Email', widget = forms.EmailInput(attrs={'placeholder': 'Email'}))


class CustomUserCreationForm(UserCreationForm):
    username = forms.EmailField(max_length = 100, required = True, label = 'Email')
    first_name = forms.CharField(max_length = 100, required = True, label = 'Jméno')
    last_name = forms.CharField(max_length = 100, required = True, label = 'Příjmení')
    client__phone = forms.CharField(max_length = 100, required = True, label = 'Telefon')
    terms_and_conditions = forms.BooleanField(required = True, label = mark_safe('Souhlasím s <a href="https://smart.naxter.cz/obchodni-podminky" target="_blank" class="text-muted">obchodní podmínky</a> a <a href="https://smart.naxter.cz/gdpr" target="_blank" class="text-muted">ochranou osobních údajů</a>'))
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    def save(self, *args, **kw):
#         self.instance.client = models.Client(phone=self.cleaned_data.get('client__phone'))
# #         self.instance.client.save()
#         self.instance.save()

        self.instance.email = self.instance.username

        return super(CustomUserCreationForm, self).save(*args, **kw)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']


class CustomUserProfileForm(forms.ModelForm):
    email = forms.CharField(max_length = 100, required = True, label = 'Email', widget=forms.TextInput())
    first_name = forms.CharField(max_length = 100, required = True, label = 'Jméno', widget=forms.TextInput())
    last_name = forms.CharField(max_length = 100, required = True, label = 'Příjmení', widget=forms.TextInput())
    client__phone = forms.CharField(max_length = 100, required = False, label = 'Telefon', widget = forms.TextInput())
    client__outage_notification = forms.BooleanField(required = False, label = 'Informovat mne o výpadku')
    password1 = forms.CharField(max_length = 100, required = False, label = 'Nové heslo', widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 100, required = False, label = 'Potvrzení hesla', widget = forms.PasswordInput())

    def __init__(self, *args, **kw):
        super(CustomUserProfileForm, self).__init__(*args, **kw)
        self.fields['email'].initial = self.instance.email
        self.fields['first_name'].initial = self.instance.first_name
        self.fields['last_name'].initial = self.instance.last_name
        self.fields['client__phone'].initial = self.instance.client.phone
        self.fields['client__outage_notification'].initial = self.instance.client.outage_notification

    def save(self, *args, **kw):
#         super(CustomUserProfileForm, self).save(*args, **kw)

        self.instance.client.phone = self.cleaned_data.get('client__phone')
        self.instance.client.outage_notification = self.cleaned_data.get('client__outage_notification')
        self.instance.client.save()

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != "" and password1 == password2:
            self.instance.set_password(password1)

        self.instance.email = self.cleaned_data.get('email')
        self.instance.first_name = self.cleaned_data.get('first_name')
        self.instance.last_name = self.cleaned_data.get('last_name')
        self.instance.save()

        return super(CustomUserProfileForm, self).save(*args, **kw)
#         return self.instance

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']


class CustomUserDeviceForm(forms.ModelForm):
    device_brand = forms.CharField(max_length = 100, required = False, disabled = True, label = 'Značka', widget=forms.TextInput())
    device_model = forms.CharField(max_length = 100, required = False, disabled = True, label = 'Model', widget=forms.TextInput())
    device_mac = forms.CharField(max_length = 17, required = True, label = 'Kód zařízení', widget=forms.TextInput())
    device_password = forms.CharField(max_length = 100, required = True, label = 'Heslo zařízení', widget=forms.TextInput())
    name = forms.CharField(max_length = 100, required = True, label = 'Název', widget=forms.TextInput())
    address_street = forms.CharField(max_length = 100, required = False, label = 'Ulice', widget=forms.TextInput())
    address_city = forms.CharField(max_length = 100, required = False, label = 'Město', widget=forms.TextInput())
    address_postal_code = forms.CharField(max_length = 100, required = False, label = 'PSČ', widget=forms.TextInput())
    address_country = forms.CharField(max_length = 100, required = False, label = 'Země', widget=forms.TextInput())

    def __init__(self, *args, **kw):
        super(CustomUserDeviceForm, self).__init__(*args, **kw)

        if self.instance.device.id != None:
            self.fields['device_brand'].initial = self.instance.device.brand
            self.fields['device_brand'].disabled = True
            self.fields['device_model'].initial = self.instance.device.model
            self.fields['device_model'].disabled = True
            
            self.fields['device_mac'].initial = self.instance.device.mac
            self.fields['device_mac'].disabled = True
            self.fields['device_password'].initial = self.instance.device.password

            if self.instance.device.user != None and self.instance.device.user.id != self.instance.user.id:
                self.fields['device_password'].disabled = True

        self.fields['name'].initial = self.instance.name
        self.fields['address_street'].initial = self.instance.address_street
        self.fields['address_city'].initial = self.instance.address_city
        self.fields['address_postal_code'].initial = self.instance.address_postal_code
        self.fields['address_country'].initial = self.instance.address_country

    def clean(self):
        cleaned_data = super(CustomUserDeviceForm, self).clean()
        device_mac = cleaned_data.get('device_mac')
        device_password = cleaned_data.get('device_password')
        device = models.Device.objects.filter(mac = device_mac).first()
        user_device = models.UserDevice.objects.filter(device__mac = device_mac, user__id = self.instance.user.id).first()

        if device != None:
            if device.user != None and device.password != device_password:
                self.add_error('device_password', forms.ValidationError("Zařízení již využívá jiný uživatel, je potřeba zadat jím definované heslo!"))
        else:
            self.add_error('device_mac', forms.ValidationError("Nelze přidat neznámé zařízení!"))

        if user_device != None and self.instance.id == None:
            self.add_error('device_mac', forms.ValidationError("Zařízení již využíváte!"))

    def save(self, *args, **kw):
        if self.instance.device.id == None:
            device = models.Device.objects.filter(mac = self.cleaned_data.get('device_mac')).first()

            if device != None:
                if device.user == None or device.password == self.cleaned_data.get('device_password'):
                    self.instance.device = device

                    if self.instance.device.user == None:
                        self.instance.device.user = self.instance.user

            else:
                self.instance.device.mac = self.cleaned_data.get('device_mac')

        if self.instance.device.user.id == self.instance.user.id:
            self.instance.device.password = self.cleaned_data.get('device_password')

        if self.instance.device.name == None:
            self.instance.device.name = self.cleaned_data.get('name')

        x = self.instance.device.save()

        self.instance.name = self.cleaned_data.get('name')
        self.instance.address_street = self.cleaned_data.get('address_street')
        self.instance.address_city = self.cleaned_data.get('address_city')
        self.instance.address_postal_code = self.cleaned_data.get('address_postal_code')
        self.instance.address_country = self.cleaned_data.get('address_country')

        self.instance.save()

        return super(CustomUserDeviceForm, self).save(*args, **kw)

    class Meta:
        model = models.UserDevice
        fields = ['name', 'address_street', 'address_city', 'address_postal_code', 'address_country']


class CustomDeviceCronForm(forms.ModelForm):
    hour = forms.ChoiceField(choices=models.DeviceCron.HOUR_CHOICES)
    minute = forms.ChoiceField(choices=models.DeviceCron.MINUTE_CHOICES)
    action = forms.ChoiceField(choices=models.DeviceCron.ACTION_CHOICES)

    class Meta:
        model = models.DeviceCron
        fields = ['hour', 'minute', 'action'] # 'day_of_week', 'day_of_month',
