from django import forms
from .models import Comentario2, Estudio, Actividad, Tipo, Area, Maquina, ArchivoCompartido
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.contrib.auth import password_validation


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = [
            "nombre",
            "descripcion",
            "tipo",
            "color",
        ]
        widgets = {
            "tipo": forms.Select(),  
        }
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))
    vueltas = forms.CharField(required=False, widget=forms.HiddenInput())
    
    def __init__(self, *args, **kwargs):
        super(ActividadForm, self).__init__(*args, **kwargs)
        # Utiliza widgets ModelChoiceField para los campos ForeignKey
        self.fields["tipo"].widget = forms.Select()


class EstudioForm(forms.ModelForm):
    class Meta:
        model = Estudio
        fields = ["nombre", "descripcion", "fecha", "area", "maquina"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "area": forms.Select(),
            "maquina": forms.Select(),
        }   

    def __init__(self, *args, **kwargs):
        super(EstudioForm, self).__init__(*args, **kwargs)
        # Utiliza widgets ModelChoiceField para los campos ForeignKey
        self.fields["maquina"].widget = forms.Select(choices=Maquina.objects.all())
        self.fields["area"].widget = forms.Select(choices=Area.objects.all())


class EditarActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ["nombre", "descripcion", "tipo", "color"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
        }


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    # email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            # "email",
            "password1",
            "password2",
        )
        widgets = {
            'username': forms.TextInput(attrs={ 'placeholder' : 'Usuario','class': 'w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white'}),
            'last_name': forms.TextInput(attrs={ 'placeholder' : 'Usuario','class': 'w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white'}),
            # 'email': forms.EmailInput(attrs={ 'placeholder' : 'Usuario','class': 'w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white'}),
            'password1': forms.TextInput(attrs={ 'placeholder' : 'Usuario','class': 'w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white'}),
            'password2': forms.TextInput(attrs={ 'placeholder' : 'Usuario','class': 'w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white'}),

        }


class PerfilForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'image']
        widgets = {
            'first_name': forms.TextInput(attrs={ 'placeholder' : 'Usuario','class': 'appearance-none block w-full bg-grey-lighter text-grey-darker border border-grey-lighter rounded py-3 px-4'}),
            'username': forms.TextInput(attrs={ 'placeholder' : 'Usuario','class': 'appearance-none block w-full bg-grey-lighter text-grey-darker border border-grey-lighter rounded py-3 px-4 mb-3'}),
            'last_name': forms.TextInput(attrs={ 'placeholder' : 'Usuario','class': 'appearance-none block w-full bg-grey-lighter text-grey-darker border border-grey-lighter rounded py-3 px-4'}),
            'email': forms.EmailInput(attrs={ 'placeholder' : 'Usuario','class': 'appearance-none block w-full bg-grey-lighter text-grey-darker border border-grey-lighter rounded py-3 px-4'}),
            'password1': forms.TextInput(attrs={ 'placeholder' : 'Usuario','class': 'appearance-none block w-full bg-grey-lighter text-grey-darker border border-grey-lighter rounded py-3 px-4'}),
            'password2': forms.TextInput(attrs={ 'placeholder' : 'Usuario','class': 'appearance-none block w-full bg-grey-lighter text-grey-darker border border-grey-lighter rounded py-3 px-4'}),
            'image': forms.ClearableFileInput(attrs={'class': 'appearance-none block w-full bg-grey-lighter text-grey-darker border border-grey-lighter rounded py-3 px-4'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)
        self.fields['username'].widget.attrs['autocomplete'] = 'off'
        self.fields['username'].help_text = ''  # Eliminar el mensaje de ayuda predeterminado
        # Puedes añadir un mensaje personalizado si lo deseas
        # self.fields['username'].help_text = 'Tu mensaje personalizado aquí'

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("El campo 'Nombre' no puede estar vacío.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError("El campo 'Apellido' no puede estar vacío.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("El campo 'Correo electrónico' no puede estar vacío.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("El campo 'Nombre de usuario' no puede estar vacío.")
        return username

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if not hasattr(image, 'content_type') or not image.content_type.startswith('image'):
                raise forms.ValidationError('El archivo no es una imagen válida.')
        return image


class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = ['nombre']
        exclude = ['usuario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full h-8 border-black rounded-md'}),
        }

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre']
        exclude = ['usuario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full h-8 border-black rounded-md'}),
        }      


class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['nombre']
        exclude = ['usuario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full h-8 border-black rounded-md'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].error_messages = {'required': f"El campo '{field_name.capitalize()}' no puede estar vacío."}

    def clean_new_password2(self):
        password2 = super().clean_new_password2()
        try:
            password_validation.validate_password(password2, self.user)
        except forms.ValidationError as error:
            self.add_error('new_password2', error)
        return password2
    
class ComentarioForm2(forms.ModelForm):
    class Meta:
        model = Comentario2
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 2, 'cols': 50, 'class': 'mi-textarea'}),
        }
    

class ArchivoCompartidoForm(forms.ModelForm):
    class Meta:
        model = ArchivoCompartido
        fields = ['archivo']

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if not archivo:
            raise forms.ValidationError("Debes adjuntar un archivo.")
        return archivo
    
    