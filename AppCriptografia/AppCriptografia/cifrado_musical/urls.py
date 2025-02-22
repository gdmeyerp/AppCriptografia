from django.urls import path
from . import views
from .views import encriptar_midi
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
app_name = 'cifrado_musical'

urlpatterns = [
    path('', views.index, name='index'),
    path('cifrar/', views.cifrar_partitura_view, name='cifrar'),
    path("encriptar_midi/", encriptar_midi, name="encriptar_midi"),
    path('crear_midi/', views.crear_midi, name='crear_midi'),

    path('descifrar/', views.descifrar_partitura_view, name='descifrar'),
    path('historial/', views.historial_partituras_view, name='historial'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)