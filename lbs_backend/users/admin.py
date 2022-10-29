from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import Gender, CustomUser


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = (
            'mobileNumber', 'idNumber', 'genderID',
            'yearOfBirth', 'firstName', 'middleName',
            'surName', 'locationID', 'adBalance', 'avatar'
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("password didn't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = (
            'mobileNumber', 'idNumber', 'genderID',
            'yearOfBirth', 'firstName', 'middleName', 'avatar',
            'surName', 'locationID', 'adBalance', 'password', 'is_active', 'is_admin'
        )


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        "id", 'mobileNumber', 'idNumber', 'genderID', 'yearOfBirth', 'avatar',
        'firstName', 'middleName', 'surName', 'locationID', 'adBalance'
    )
    list_filter = ('is_admin',)
    fieldsets = (
        ('Authentication', {'fields': ('mobileNumber', 'password')}),
        ('Personal Info', {
            'fields': ('firstName', 'middleName', 'surName', 'locationID', 'adBalance',
                       'yearOfBirth', 'genderID', 'avatar'
                       )
        }),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'mobileNumber', 'idNumber', 'genderID', 'yearOfBirth',
                'firstName', 'middleName', 'surName', 'locationID', 'adBalance',
                'password1', 'password2'
            ),
        }),
    )

    search_fields = ('mobileNumber',)
    ordering = ('mobileNumber',)
    filter_horizontal = ()


class GenderAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name"
    ]


admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Gender, GenderAdmin)
