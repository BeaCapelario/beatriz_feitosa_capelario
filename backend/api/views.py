from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from .models import Locais, Responsaveis, Ambientes, Sensores, Historico
from .serializers import (
    LocaisSerializer,
    ResponsaveisSerializer,
    AmbientesSerializer,
    SensoresSerializer,
    HistoricoSerializer,
    RegisterSerializer
)
from .filters import (
    LocaisFilter,
    ResponsaveisFilter,
    AmbientesFilter,
    SensoresFilter,
    HistoricoFilter
)
# ==================== Locais ==================== #
class LocaisView(ListCreateAPIView):
    queryset = Locais.objects.all()
    serializer_class = LocaisSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id']               
    search_fields = ['id', 'local']  
    ordering_fields = ['id', 'local'] 
    ordering = ['local']
    filterset_class = LocaisFilter  
    
class LocaisDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Locais.objects.all()
    serializer_class = LocaisSerializer
    permission_classes =[IsAuthenticated]

# ==================== Responsáveis ==================== #
class ResponsaveisView(ListCreateAPIView):
    queryset = Responsaveis.objects.all()
    serializer_class = ResponsaveisSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id']               
    search_fields = ['id', 'nome']  
    ordering_fields = ['id', 'nome'] 
    ordering = ['nomel']
    filterset_class = LocaisFilter  

class ResponsaveisDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Responsaveis.objects.all()
    serializer_class = ResponsaveisSerializer
    permission_classes =[IsAuthenticated]

# ==================== Ambientes ==================== #
class AmbientesView(ListCreateAPIView):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id']               
    search_fields = ['id', 'descricao']  
    ordering_fields = ['id', 'descricao'] 
    ordering = ['descricao']
    filterset_class = LocaisFilter  
    
class AmbientesDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer
    permission_classes =[IsAuthenticated]

# ==================== Sensores ==================== #
class SensoresView(ListCreateAPIView):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id']               
    search_fields = ['id', 'sensor' , 'mac_address' , 'status']  
    ordering_fields = ['id', 'sensor'] 
    ordering = ['sensor']
    filterset_class = LocaisFilter  

class SensoresDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer
    permission_classes =[IsAuthenticated]

# ==================== Histórico ==================== #
class HistoricoView(ListCreateAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
 
class HistoricoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    
 # ==================== Register ==================== #   

class RegisterView(ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': {'id': user.id, 'username': user.username},
            'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)}
        }, status=status.HTTP_201_CREATED)

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class LocaisViewSet(ModelViewSet):
    queryset = Locais.objects.select_related("local").order_by("-id")
    serializer_class = LocaisSerializer
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["id", "local"]
    ordering_fields = ["id", "local"]
    ordering = ["local"]
    
class ResponsaveisViewSet(ModelViewSet):
    queryset = Responsaveis.objects.select_related("nome").order_by("-id")
    serializer_class = ResponsaveisSerializer
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["nome"]
    ordering_fields = ["id", "nome"]
    ordering = ["nome"]

class AmbientesViewSet(ModelViewSet):
    queryset = Ambientes.objects.select_related("descricao").order_by("-id")
    serializer_class = AmbientesSerializer
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["descricao"]
    ordering_fields = ["id", "descricao"]
    ordering = ["descricao"]
    
class SensoresViewSet(ModelViewSet):
    queryset = Sensores.objects.select_related("local").order_by("-id")
    serializer_class = SensoresSerializer
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["sensor", "mac_address", "status"]
    ordering_fields = ["id", "sensor"]
    ordering = ["sensor"]