from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Estudios.models import Profile

class Command(BaseCommand):
    help = 'Creates profiles for existing users'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            Profile.objects.get_or_create(user=user)
