# cultivos/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Avg, Max, Min, Count
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .models import Cultivo, HistorialPrecio
import openpyxl
from datetime import datetime

# Vista para la página de inicio
def inicio(request):
    """Vista para la página de inicio"""
    total_cultivos = Cultivo.objects.count()
    cultivos_recientes = Cultivo.objects.order_by('-id')[:5]
    
    # Obtener precios recientes para el gráfico simple
    cultivos = Cultivo.objects.all()[:10]
    
    context = {
        'total_cultivos': total_cultivos,
        'cultivos_recientes': cultivos_recientes,
        'cultivos': cultivos,
        'titulo': 'Inicio - AgroControl'
    }
    return render(request, 'inicio.html', context)

# Vista para listar todos los cultivos
def lista_cultivos(request):
    """Vista para listar todos los cultivos"""
    cultivos = Cultivo.objects.all().order_by('nombre')
    
    context = {
        'cultivos': cultivos,
        'total_cultivos': cultivos.count(),
        'titulo': 'Lista de Cultivos - AgroControl'
    }
    return render(request, 'cultivos/lista.html', context)

# API para datos de gráficos
def estadisticas_api(request):
    """API para datos de gráficos"""
    cultivos = Cultivo.objects.all()
    
    precios_data = {
        'labels': [c.nombre for c in cultivos],
        'precios': [float(c.precio) for c in cultivos],
        'cantidades': [c.cantidad for c in cultivos]
    }
    
    stats = {
        'total_cultivos': cultivos.count(),
        'precio_promedio': cultivos.aggregate(Avg('precio'))['precio__avg'] or 0,
        'cantidad_total': cultivos.aggregate(Sum('cantidad'))['cantidad__sum'] or 0,
        'precio_maximo': cultivos.aggregate(Max('precio'))['precio__max'] or 0,
    }
    
    return JsonResponse({'precios': precios_data, 'stats': stats})

# Dashboard completo
def dashboard_completo(request):
    """Dashboard con estadísticas"""
    cultivos = Cultivo.objects.all()
    total_cultivos = cultivos.count()
    
    # Estadísticas básicas
    precio_promedio = cultivos.aggregate(Avg('precio'))['precio__avg'] or 0
    cantidad_total = cultivos.aggregate(Sum('cantidad'))['cantidad__sum'] or 0
    precio_maximo = cultivos.aggregate(Max('precio'))['precio__max'] or 0
    
    # Calcular valor total del inventario
    valor_total = sum(c.precio * c.cantidad for c in cultivos) if cultivos else 0
    
    # Cultivos por temporada
    temporadas_data = {}
    for cultivo in cultivos:
        temp = cultivo.get_temporada_siembra_display()
        temporadas_data[temp] = temporadas_data.get(temp, 0) + 1
    
    # Cultivos por tipo
    tipos_data = {}
    for cultivo in cultivos:
        tipo = cultivo.get_tipo_display()
        tipos_data[tipo] = tipos_data.get(tipo, 0) + 1
    
    # Top cultivos por valor
    cultivos_lista = list(cultivos)
    cultivos_lista.sort(key=lambda x: x.precio * x.cantidad, reverse=True)
    top_cultivos = cultivos_lista[:5]
    
    context = {
        'total_cultivos': total_cultivos,
        'precio_promedio': round(precio_promedio, 2),
        'cantidad_total': cantidad_total,
        'precio_maximo': round(precio_maximo, 2),
        'valor_total_inventario': round(valor_total, 2),
        'temporadas': temporadas_data,
        'tipos': tipos_data,
        'cultivo_mas_caro': cultivos.order_by('-precio').first(),
        'top_cultivos': top_cultivos,
        'cultivos_recientes': cultivos.order_by('-id')[:5],
    }
    return render(request, 'dashboard.html', context)

# Búsqueda y filtros avanzados
def buscar_cultivos(request):
    """Búsqueda y filtros avanzados"""
    cultivos = Cultivo.objects.all()
    
    query = request.GET.get('q', '')
    if query:
        cultivos = cultivos.filter(nombre__icontains=query)
    
    temporada = request.GET.get('temporada', '')
    if temporada:
        cultivos = cultivos.filter(temporada_siembra=temporada)
    
    tipo = request.GET.get('tipo', '')
    if tipo:
        cultivos = cultivos.filter(tipo=tipo)
    
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    if precio_min:
        cultivos = cultivos.filter(precio__gte=precio_min)
    if precio_max:
        cultivos = cultivos.filter(precio__lte=precio_max)
    
    context = {
        'cultivos': cultivos,
        'total_cultivos': cultivos.count(),
        'query': query,
        'tipos': Cultivo.TIPOS,
        'temporadas': Cultivo.TEMPORADAS,
    }
    return render(request, 'cultivos/buscar.html', context)

# Exportar a Excel
def exportar_excel(request):
    """Exportar cultivos a Excel"""
    cultivos = Cultivo.objects.all()
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cultivos"
    
    headers = ['Nombre', 'Tipo', 'Región', 'Precio', 'Cantidad', 'Valor Total', 'Temporada de Siembra', 'Temporada de Cosecha']
    ws.append(headers)
    
    for c in cultivos:
        ws.append([
            c.nombre,
            c.get_tipo_display(),
            c.region,
            float(c.precio),
            c.cantidad,
            float(c.valor_total),
            c.get_temporada_siembra_display(),
            c.get_temporada_cosecha_display()
        ])
    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=cultivos.xlsx'
    wb.save(response)
    return response

# Calendario de siembra
def calendario_siembra(request):
    """Calendario de siembra por mes"""
    cultivos = Cultivo.objects.all()
    
    temporada_meses = {
        'PRIMAVERA': ['Marzo', 'Abril', 'Mayo'],
        'VERANO': ['Junio', 'Julio', 'Agosto'],
        'OTOÑO': ['Septiembre', 'Octubre', 'Noviembre'],
        'INVIERNO': ['Diciembre', 'Enero', 'Febrero'],
        'TODO_EL_AÑO': ['Todo el año']
    }
    
    calendario = []
    for cultivo in cultivos:
        meses = temporada_meses.get(cultivo.temporada_siembra, [])
        calendario.append({
            'cultivo': cultivo,
            'meses': meses,
            'temporada': cultivo.get_temporada_siembra_display()
        })
    
    context = {
        'calendario': calendario,
        'total_cultivos': len(calendario),
    }
    return render(request, 'cultivos/calendario.html', context)

# Comparar cultivos
def comparar_cultivos(request):
    """Compara dos cultivos lado a lado"""
    cultivo1_id = request.GET.get('cultivo1')
    cultivo2_id = request.GET.get('cultivo2')
    
    cultivos = Cultivo.objects.all()
    cultivo1 = None
    cultivo2 = None
    
    if cultivo1_id:
        cultivo1 = Cultivo.objects.filter(id=cultivo1_id).first()
    if cultivo2_id:
        cultivo2 = Cultivo.objects.filter(id=cultivo2_id).first()
    
    context = {
        'cultivos': cultivos,
        'cultivo1': cultivo1,
        'cultivo2': cultivo2,
    }
    return render(request, 'cultivos/comparar.html', context)

# Registrar precio histórico
def registrar_precio(request, cultivo_id):
    """Registra el precio actual en el historial"""
    cultivo = get_object_or_404(Cultivo, id=cultivo_id)
    HistorialPrecio.objects.create(
        cultivo=cultivo,
        precio=cultivo.precio
    )
    return JsonResponse({'success': True, 'message': 'Precio registrado en historial'})