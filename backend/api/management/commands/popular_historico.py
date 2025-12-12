from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Sensores, Historico
import random


class Command(BaseCommand):
    help = "Popula o histórico com valores aleatórios para todos os sensores"

    def handle(self, *args, **options):

        sensores = Sensores.objects.all()

        if not sensores.exists():
            self.stdout.write(self.style.ERROR("Nenhum sensor encontrado!"))
            return

        historicos = []

        for sensor in sensores:
            historicos.append(
                Historico(
                    sensor=sensor,
                    valor=random.uniform(10, 40),
                    timestamp=timezone.now()
                )
            )

        Historico.objects.bulk_create(historicos)

        self.stdout.write(self.style.SUCCESS(
            f"Histórico populado com sucesso! Registros criados: {len(historicos)}"
        ))
