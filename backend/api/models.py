from django.db import models
# ==================== Locais ==================== #
class Locais(models.Model):
    local = models.CharField(max_length=100)

    def __str__(self):
        return self.local

# ==================== Responsáveis ==================== #
class Responsaveis(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
# ==================== Ambientes ==================== #
class Ambientes(models.Model):
    local = models.ForeignKey(Locais, on_delete=models.CASCADE)
    descricao = models.TextField(max_length=100)
    nome = models.ForeignKey(Responsaveis, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao
    
# ==================== Sensores ==================== #
class Sensores(models.Model):
    sensor = models.CharField(max_length=50)
    mac_address = models.CharField(max_length=17, unique=True)
    unidade_medida = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.BooleanField(default=True)
    ambiente = models.ForeignKey(Ambientes, on_delete=models.CASCADE)

    def __str__(self):
        return self.sensor

# ==================== Histórico ==================== #
class Historico(models.Model):
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    ambiente = models.ForeignKey(Ambientes, on_delete=models.CASCADE)
    valor = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor} - {self.valor} ({self.timestamp:%d/%m/%Y %H:%M:%S})"