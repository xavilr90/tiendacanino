from django import forms
from .models import Mascota
from django.contrib.auth.models import User, Group


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = [
            'raza',
            'tamaño',
            'asesor',
            'descripcion'
        ]

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Seleccione un grupo",
        required=True,
        label="Tipo de usuario"
    )

    class Meta:
        model = User
        fields = ['username', 
                  'email', 
                  'password',
                  'group'
                ]
