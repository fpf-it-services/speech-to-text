from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
import assemblyai as aai
import os
from django.http import JsonResponse

# Configurez l'API Key d'AssemblyAI
aai.settings.api_key = "a6d31e8ed3c141529da0e65781508992"
config = aai.TranscriptionConfig(language_code="fr")

@api_view(['POST'])
def transcribe_audio(request):
    # Récupère le fichier audio envoyé dans le corps de la requête
    audio_file = request.FILES.get('audio')

    if not audio_file:
        return JsonResponse({'error': 'Aucun fichier audio envoyé.'}, status=400)

    # Enregistre l'audio dans un dossier temporaire
    audio_path = os.path.join('media', 'audio.wav')
    
    with open(audio_path, 'wb') as f:
        for chunk in audio_file.chunks():
            f.write(chunk)

    # Utilise AssemblyAI pour la transcription
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(audio_path)

    if transcript.status == aai.TranscriptStatus.error:
        os.remove(audio_path)  # Supprime le fichier si la transcription échoue
        return JsonResponse({'error': f'Transcription échouée : {transcript.error}'}, status=500)

    # Supprime le fichier audio après transcription
    os.remove(audio_path)
    print(transcript.text)

    data = {
        "message": transcript.text,
        "status": "success"
    }
    return Response(data)
