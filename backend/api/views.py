from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Locais, Responsaveis, Ambientes, Sensores, Historico
from .serializers import LocaisSerializer, ResponsaveisSerializer, AmbientesSerializer, SensoresSerializer, HistoricoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# ==================== Locais ==================== #
class LocaisView(ListCreateAPIView):
    queryset = Locais.objects.all()
    serializer_class = LocaisSerializer

# ==================== Responsáveis ==================== #
class ResponsaveisView(ListCreateAPIView):
    queryset = Responsaveis.objects.all()
    serializer_class = ResponsaveisSerializer

# ==================== Ambientes ==================== #
class AmbientesView(ListCreateAPIView):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer

# ==================== Sensores ==================== #
class SensoresView(ListCreateAPIView):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer

# ==================== Histórico ==================== #
class HistoricoView(ListCreateAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    
# ==================== Login ==================== #

        