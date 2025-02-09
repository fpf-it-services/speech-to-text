from django.urls import path
from . import views

urlpatterns = [
    path('api/transcribe/', views.transcribe_audio, name='transcribe_audio'),
    path('api/translate/<str:target_language>/', views.translate_to_local_language, name='translate')
    # Exemple d'URL : /translate/goun/
]
