from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
import assemblyai as aai
import os
from django.http import JsonResponse
from google import genai


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
    
    

    # client = genai.Client(api_key="AIzaSyB9AhT3ROhLlPrmTbKiChwUQZ913SiDfoU")
    # response = client.models.generate_content(
    #     model="gemini-2.0-flash", contents=f'Traduit en langue {target_language} ceci sans markdown: {transcript.text}'
    # )
    # print(response.text)


    data = {
        "message": transcript.text,
        "status": "success"
    }
    return Response(data)

@api_view(['POST'])
def translate_to_local_language(request, target_language):
    text = request.data.get('text')

    if not text:
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