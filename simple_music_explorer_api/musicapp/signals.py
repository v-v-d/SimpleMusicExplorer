from django.db.models.signals import post_save
from django.dispatch import receiver
from mutagen import File

from musicapp.models import AlbumTrack


@receiver(post_save, sender=AlbumTrack)
def calculate_track_duration(sender, instance, **kwargs):
    file_model = instance.audio_file.first()

    if file_model:
        audio_info = File(instance.audio_file.first().file).info
        instance.duration = audio_info.length
