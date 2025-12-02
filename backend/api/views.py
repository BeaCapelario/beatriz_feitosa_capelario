from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.timezone import now
from datetime import timedelta

from .models import Locais, Responsaveis, Ambientes, Sensores, Historico
from .serializers import (
    LocaisSerializer, ResponsaveisSerializer, AmbientesSerializer,
    SensoresSerializer, HistoricoSerializer, RegisterSerializer,
)
from .filters import (
    LocaisFilter, ResponsaveisFilter,
    AmbientesFilter, SensoresFilter, HistoricoFilter, MedicoesFilter
)

# ==================== Locais ==================== #
class LocaisView(ListCreateAPIView):
    queryset = Locais.objects.all()
    serializer_class = LocaisSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = LocaisFilter
    search_fields = ['id', 'local']
    ordering_fields = ['id', 'local']
    ordering = ['local']

class LocaisDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Locais.objects.all()
    serializer_class = LocaisSerializer
    permission_classes = [IsAuthenticated]


# ==================== Responsáveis ==================== #
class ResponsaveisView(ListCreateAPIView):
    queryset = Responsaveis.objects.all()
    serializer_class = ResponsaveisSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ResponsaveisFilter
    search_fields = ['id', 'nome']
    ordering_fields = ['id', 'nome']
    ordering = ['nome']

class ResponsaveisDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Responsaveis.objects.all()
    serializer_class = ResponsaveisSerializer
    permission_classes = [IsAuthenticated]


# ==================== Ambientes ==================== #
class AmbientesView(ListCreateAPIView):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AmbientesFilter
    search_fields = ['id', 'descricao']
    ordering_fields = ['id', 'descricao']
    ordering = ['descricao']

class AmbientesDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer
    permission_classes = [IsAuthenticated]


# ==================== Sensores ==================== #
class SensoresView(ListCreateAPIView):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SensoresFilter
    search_fields = ['id', 'sensor', 'mac_address', 'status']
    ordering_fields = ['id', 'sensor']
    ordering = ['sensor']

class SensoresDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer
    permission_classes = [IsAuthenticated]


# ==================== Histórico ==================== #
class HistoricoView(ListCreateAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    permission_classes = [AllowAny]

class HistoricoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    permission_classes = [IsAuthenticated]


# ==================== Registro de Usuário ==================== #
class RegisterView(ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_201_CREATED)


# ==================== Medições ==================== #
class MedicoesView(ListCreateAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MedicoesFilter
    search_fields = ['sensor__sensor']
    ordering_fields = ['id', 'timestamp']
    ordering = ['-id']

    def create(self, request, *args, **kwargs):
        sensor_id = request.data.get("sensor")

        if not sensor_id:
            return Response({"erro": "sensor é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sensor = Sensores.objects.get(id=sensor_id)
        except Sensores.DoesNotExist:
            return Response({"erro": "Sensor não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Bloquear registro se o sensor estiver inativo
        if not sensor.status:
            return Response({"erro": "Não é possível registrar medições para um sensor inativo."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class MedicoesPorSensorView(ListAPIView):
    serializer_class = HistoricoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        sensor_id = self.kwargs["sensor_id"]
        return Historico.objects.filter(sensor_id=sensor_id).order_by("-timestamp")


class MedicoesRecentesView(ListAPIView):
    serializer_class = HistoricoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        hours = int(self.request.query_params.get("hours", 24))
        limite = now() - timedelta(hours=hours)
        return Historico.objects.filter(timestamp__gte=limite).order_by("-timestamp")
