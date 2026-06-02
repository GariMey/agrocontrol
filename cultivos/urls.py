# cultivos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('cultivos/', views.lista_cultivos, name='lista_cultivos'),
    path('api/estadisticas/', views.estadisticas_api, name='estadisticas_api'),
    path('dashboard/', views.dashboard_completo, name='dashboard_completo'),
    path('buscar/', views.buscar_cultivos, name='buscar_cultivos'),
    path('exportar/', views.exportar_excel, name='exportar_excel'),
    path('calendario/', views.calendario_siembra, name='calendario_siembra'),
    path('comparar/', views.comparar_cultivos, name='comparar_cultivos'),
    path('registrar-precio/<int:cultivo_id>/', views.registrar_precio, name='registrar_precio'),
]