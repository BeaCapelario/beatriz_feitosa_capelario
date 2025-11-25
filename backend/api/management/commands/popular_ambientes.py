import pandas as pd
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Locais, Responsaveis, Ambientes

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--arquivo-locais", default="./population/locais.csv")
        parser.add_argument("--arquivo-responsaveis", default="./population/nomes.csv")
        parser.add_argument("--arquivo-ambientes", default="./population/ambientes.csv")
        
        parser.add_argument("--truncate", action="store_true")
        parser.add_argument("--update", action="store_true")
        
    @transaction.atomic
    def handle(self, *a, **o):
        df_locais = pd.read_csv(o["arquivo_locais"], encoding="utf-8-sig")
        df_responsaveis = pd.read_csv(o["arquivo_responsaveis"], encoding="utf-8-sig")
        df_ambientes = pd.read_csv(o["arquivo_ambientes"], encoding="utf-8-sig")
        
        df_locais.columns = [c.strip().lower().lstrip("\ufeff") for c in df_locais.columns]
        df_responsaveis.columns = [c.strip().lower().lstrip("\ufeff") for c in df_responsaveis.columns]
        df_ambientes.columns = [c.strip().lower().lstrip("\ufeff") for c in df_ambientes.columns]
        
        df_locais = df_locais.drop_duplicates(subset=['local'])
        df_responsaveis = df_responsaveis.drop_duplicates(subset=['nome'])
        
        df_locais['id_local'] = df_locais.index + 1
        mapa_locais = dict(zip(df_locais['id_local'], df_locais['local']))
        df_ambientes['local_nome'] = df_ambientes['local'].map(mapa_locais)
        
        df_responsaveis['id_responsavel'] = df_responsaveis.index + 1 
        mapa_responsaveis = dict(zip(df_responsaveis['id_responsavel'], df_responsaveis['nome']))
        df_ambientes['responsavel_nome'] = df_ambientes['responsavel'].map(mapa_responsaveis)
        
        if o["truncate"]:
            Ambientes.objects.all().delete()
            Locais.objects.all().delete()
            Responsaveis.objects.all().delete()
            
        df_ambientes['descricao'] = df_ambientes['descricao'].astype(str).str.strip()
        df_ambientes['local_nome'] = df_ambientes['local_nome'].astype(str).str.strip()
        df_ambientes['responsavel_nome'] = df_ambientes['responsavel_nome'].astype(str).str.strip()
        

        for r in df_locais.itertuples(index=False):
            Locais.objects.update_or_create(
                local=r.local,
                defaults={'local': r.local}
            )
        
        for r in df_responsaveis.itertuples(index=False):
            Responsaveis.objects.update_or_create(
                nome=r.nome,
                defaults={'nome': r.nome}
            )
        
        locais_dict = {local.local: local for local in Locais.objects.all()}
        responsaveis_dict = {responsavel.nome: responsavel for responsavel in Responsaveis.objects.all()}
        
        if o["update"]:
            criados = atualizados = 0
            for r in df_ambientes.itertuples(index=False):
                local_obj = locais_dict.get(r.local_nome)
                responsavel_obj = responsaveis_dict.get(r.responsavel_nome)
                
                if local_obj and responsavel_obj:
                    _, created = Ambientes.objects.update_or_create(
                        descricao=r.descricao,
                        defaults={
                            "local": local_obj,
                            "nome": responsavel_obj,
                            "descricao": r.descricao,
                        },
                    )
                    
                    criados += int(created)
                    atualizados += int(not created)
                else:
                    self.stdout.write(self.style.WARNING(f"Local ou Responsável não encontrado para: {r.descricao}"))
                
            self.stdout.write(self.style.SUCCESS(f"Criados: {criados} | Atualizados: {atualizados}"))
        
        else:
            objs = []
            for r in df_ambientes.itertuples(index=False):
                local_obj = locais_dict.get(r.local_nome)
                responsavel_obj = responsaveis_dict.get(r.responsavel_nome)
                
                if local_obj and responsavel_obj:
                    objs.append(
                        Ambientes(
                            local=local_obj,
                            nome=responsavel_obj,
                            descricao=r.descricao,
                        )
                    )
                else:
                    self.stdout.write(self.style.WARNING(f"Local ou Responsável não encontrado para: {r.descricao}"))
                
            Ambientes.objects.bulk_create(objs, ignore_conflicts=True)
            criados = len(objs)
            
            self.stdout.write(self.style.SUCCESS(f"Criados: {len(objs)}"))