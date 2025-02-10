from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
import assemblyai as aai
import os
from django.http import JsonResponse
from google import genai

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

aai.settings.api_key = "a6d31e8ed3c141529da0e65781508992"
config = aai.TranscriptionConfig(language_code="fr")

@api_view(['POST'])
def transcribe_audio(request):
    audio_file = request.FILES.get('audio')

    if not audio_file:
        return JsonResponse({'error': 'Aucun fichier audio envoyé.'}, status=400)

    audio_path = os.path.join('media', 'audio.wav')
    
    with open(audio_path, 'wb') as f:
        for chunk in audio_file.chunks():
            f.write(chunk)

    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(audio_path)

    if transcript.status == aai.TranscriptStatus.error:
        os.remove(audio_path)  
        return JsonResponse({'error': f'Transcription échouée : {transcript.error}'}, status=500)

    os.remove(audio_path)

    data = {
        "message": transcript.text,
        "status": "success"
    }
    return Response(data)

@api_view(['POST'])
def translate_to_local_language(request, target_language):
    logger.info(f"Route visitée : {request.build_absolute_uri()} - Traduction demandée en {target_language}")
    text = request.data.get('text')
    logger.info(f"Texte reçu pour traduction : {text}")

    if not text:
        logger.error("Aucun texte à traduire envoyé.")
        return JsonResponse({'error': 'Aucun texte à traduire envoyé.'}, status=400)

    try:
        client = genai.Client(api_key="AIzaSyB9AhT3ROhLlPrmTbKiChwUQZ913SiDfoU")
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=f'Traduit en langue {target_language} ceci sans markdown: {text}'
        )

        if response.text:
            data = {
                'original_text': text,
                "translation": response.text,
                'target_language': target_language,
                "status": "success"
            }
            return Response(data)
        else:
            return JsonResponse({'error': 'La traduction a échoué.'}, status=500)

    except genai.error.APIError as e:
        return JsonResponse({'error': f'Erreur de l\'API Gemini : {e}'}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'Une erreur inattendue s\'est produite : {e}'}, status=500)