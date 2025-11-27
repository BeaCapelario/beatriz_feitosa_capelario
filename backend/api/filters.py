import django_filters as df
from django.db.models import Q
from .models import Locais, Responsaveis, Ambientes, Sensores, Historico

class LocaisFilter(df.FilterSet):
    id = df.NumberFilter(field_name='id', lookup_expr='exact')
    local = df.CharFilter(field_name='local', lookup_expr='icontains')
    
    class Meta:
        model = Locais
        fields = []
        
class ResponsaveisFilter(df.FilterSet):
    id = df.NumberFilter(field_name='id', lookup_expr='exact')
    nome = df.CharFilter(field_name='nome', lookup_expr='icontains')
    
    class Meta:
        model = Responsaveis
        fields = []
        
class AmbientesFilter(df.FilterSet):
    id = df.NumberFilter(field_name='id', lookup_expr='exact')
    local = df.CharFilter(field_name='local', lookup_expr='icontains')
    descricao = df.CharFilter(field_name='descricao', lookup_expr='icontains')
    nome = df.CharFilter(field_name='nome', lookup_expr='icontains')
    
    class Meta:
        model = Ambientes
        fields = []
        
class SensoresFilter(df.FilterSet):
    id = df.NumberFilter(field_name='id', lookup_expr='exact')
    sensor = df.CharFilter(field_name='sensor', lookup_expr='icontains')
    mac_address = df.CharFilter(field_name='mac_address', lookup_expr='icontains')
    unidade_medida = df.CharFilter(field_name='unidade_medida', lookup_expr='icontains')
    latitude_min = df.NumberFilter(field_name='latitude', lookup_expr='gte')
    latitude_max = df.NumberFilter(field_name='latitude', lookup_expr='lte')
    longitude_min = df.NumberFilter(field_name='longitude', lookup_expr='gte')
    longitude_max = df.NumberFilter(field_name='longitude', lookup_expr='lte')
    status = df.BooleanFilter(field_name='status')
    ambiente = df.CharFilter(field_name='ambiente', lookup_expr='icontains')
    
    class Meta:
        model = Sensores
        fields = []
        
class HistoricoFilter(df.FilterSet):
    id = df.NumberFilter(field_name='id', lookup_expr='exact')
    sensor = df.CharFilter(field_name='sensor', lookup_expr='icontains')
    descricao = df.CharFilter(field_name='descricao', lookup_expr='icontains')
    valor = df.NumberFilter(field_name='valor')
    timestamp = df.DateTimeFilter(field_name='timestamp')
    
    class Meta:
        model = Historico
        fields = []
        
        

    