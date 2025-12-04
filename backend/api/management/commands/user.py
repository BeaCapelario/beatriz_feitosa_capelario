from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
 
class Command(BaseCommand):
    def handle(self,*args,**options):
        username = "senai"
        password = "123"
 
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username,email="",password=password)
            self.stdout.write(self.style.SUCCESS(f"Usuário {username} criado! Sua senha atual é {password}"))
        else:
            self.stdout.write(f"Usuário {username} já existe")