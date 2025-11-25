from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import LocaisView, ResponsaveisView, AmbientesView, SensoresView, HistoricoView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()

urlpatterns = [
    path('locais', LocaisView.as_view()),
    path('responsaveis', ResponsaveisView.as_view()),
    path('ambientes', AmbientesView.as_view()),
    path('sensores', SensoresView.as_view()),
    path('historico', HistoricoView.as_view()),
    
    path('token/',   TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(),     name='token_refresh'),
    
    
]




