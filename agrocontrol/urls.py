
from django.contrib import admin
from django.urls import path, include  # ← Agrega ", include"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cultivos.urls')),  # ← Agrega esta línea
]