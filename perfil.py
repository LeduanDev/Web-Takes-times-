from django.contrib.auth.models import User
from .Estudios.models import Profile

# Itera sobre los usuarios existentes y crea perfiles para ellos
for user in User.objects.all():
    Profile.objects.get_or_create(user=user)
