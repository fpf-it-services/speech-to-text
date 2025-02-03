from django.db import models

# Create your models here.

class Audio(models.Model):
    audio_file = models.FileField(upload_to='uploads/')  # Le fichier audio sera enregistré ici
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création du fichier audio

    def __str__(self):
        return f'Audio enregistré à {self.created_at}'
