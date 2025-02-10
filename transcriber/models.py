from django.db import models


class Audio(models.Model):
    audio_file = models.FileField(upload_to='uploads/')  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f'Audio enregistré à {self.created_at}'
