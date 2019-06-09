from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
import datetime

from .models import CustomUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    is_staff = forms.BooleanField(required=False)
    is_active = forms.BooleanField(required=False, initial=True)
    date_joined = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = CustomUser
        fields = ('email', 'is_staff', 'is_active', 'date_joined', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_active', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_staff', )
    # list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('fecha_nacimiento', 'nombre', 'apellido', 'dni', 'num_tarjeta_credito', 'nombre_titular_tarjeta', 'fecha_vencimiento_tarjeta', 'codigo_seguridad_tarjeta')}),
         ('Permissions', {'fields': ('is_staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'date_joined')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(CustomUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group) # para que no se administren los grupos (da igual)


































# from django.contrib import admin
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

# # from .forms import CustomUserCreationForm, CustomUserChangeForm
# from .models import CustomUser


# # class CustomUserAdmin(UserAdmin):
# #     add_form = CustomUserCreationForm
# #     form = CustomUserChangeForm
# #     model = CustomUser
# #     list_display = ('email', 'is_staff', 'is_active',)
# #     list_filter = ('email', 'is_staff', 'is_active',)
# #     fieldsets = (
# #         (None, {'fields': ('email', 'password')}),
# #         ('Permissions', {'fields': ('is_staff', 'is_active')}),
# #     )
# #     add_fieldsets = (
# #         (None, {
# #             'classes': ('wide',),
# #             'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
# #         ),
# #     )
# #     search_fields = ('email',)
# #     ordering = ('email',)


# admin.site.register(CustomUser)

