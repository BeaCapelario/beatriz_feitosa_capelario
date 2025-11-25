from rest_framework import serializers
from .models import Locais, Responsaveis, Ambientes, Sensores, Historico


# ==================== Locais ==================== #
class LocaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locais
        fields = '__all__'

# ==================== Responsáveis ==================== #
class ResponsaveisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsaveis
        fields = '__all__'

# ==================== Ambientes ==================== #
class AmbientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambientes
        fields = '__all__'

# ==================== Sensores ==================== #
class SensoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensores
        fields = '__all__'

# ==================== Histórico ==================== #
class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = '__all__'