import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from api.models import Sensores, Ambientes, Historico


class Command(BaseCommand):
    help = "Importa sensores do CSV population/sensores.csv"

    def add_arguments(self, parser):
        parser.add_argument("--arquivo_sensores", default="population/sensores.csv")
        parser.add_argument("--truncate", action="store_true", help="Apaga todos os sensores antes de importar")
        parser.add_argument("--update", action="store_true", help="Faz upsert (update_or_create)")

    @transaction.atomic
    def handle(self, *args, **options):

        df = pd.read_csv(options["arquivo_sensores"], encoding="utf-8-sig")
        df.columns = [c.strip().lower() for c in df.columns]

        df["sensor"] = df["sensor"].astype(str).str.strip()
        df["mac_address"] = df["mac_address"].astype(str).str.strip()
        df["unidade_medida"] = df["unidade_medida"].astype(str).str.strip()
        df["latitude"] = df["latitude"].astype(float)
        df["longitude"] = df["longitude"].astype(float)
        df["status"] = df["status"].astype(bool)
        df["ambiente_id"] = df["ambiente"].astype(int)

        ids_ambientes = set(Ambientes.objects.values_list("id", flat=True))
        ids_utilizados = set(df["ambiente_id"].unique())
        ids_faltando = ids_utilizados - ids_ambientes

        if ids_faltando:
            raise CommandError(f"Os seguintes ambientes NÃO existem no banco: {ids_faltando}")

        if options["truncate"]:
            Sensores.objects.all().delete()
            Historico.objects.all().delete()
            self.stdout.write(self.style.WARNING("Sensores e Histórico apagados!"))

        if options["update"]:
            criados = 0
            atualizados = 0

            for r in df.itertuples(index=False):
                sensor_obj, created = Sensores.objects.update_or_create(
                    sensor=r.sensor,
                    mac_address=r.mac_address,
                    defaults={
                        "unidade_medida": r.unidade_medida,
                        "latitude": r.latitude,
                        "longitude": r.longitude,
                        "status": r.status,
                        "ambiente_id": r.ambiente_id,
                    },
                )

                if created:
                    criados += 1
                else:
                    atualizados += 1

                Historico.objects.create(
                    sensor=sensor_obj,
                    valor=10.5,
                    timestamp=timezone.now()
                )

            self.stdout.write(self.style.SUCCESS(f"Criados: {criados} | Atualizados: {atualizados}"))
            return

        sensores_objs = []

        for r in df.itertuples(index=False):
            sensor_obj = Sensores(
                sensor=r.sensor,
                mac_address=r.mac_address,
                unidade_medida=r.unidade_medida,
                latitude=r.latitude,
                longitude=r.longitude,
                status=r.status,
                ambiente_id=r.ambiente_id,
            )
            sensores_objs.append(sensor_obj)

        Sensores.objects.bulk_create(sensores_objs, ignore_conflicts=True)

        sensores_salvos = Sensores.objects.all()

        historicos_objs = []
        for sensor in sensores_salvos:
            historicos_objs.append(
                Historico(
                    sensor=sensor,
                    valor=10.5,
                    timestamp=timezone.now()
                )
            )

        Historico.objects.bulk_create(historicos_objs)

        self.stdout.write(self.style.SUCCESS(f"Sensores inseridos: {len(sensores_salvos)}"))
        self.stdout.write(self.style.SUCCESS(f"Históricos criados: {len(historicos_objs)}"))
