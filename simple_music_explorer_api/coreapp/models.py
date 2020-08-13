from pathlib import Path

from django.db import models


class Core(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    date_modif = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f'{self.title}' if self.title else super().__str__()

    # def delete(self, **kwargs):
    #     if 'force' in kwargs:
    #         super().delete()
    #     else:
    #         self.active = False
    #         self.save()


def file_path(instance, filename):
    # file will be uploaded to the path like
    # media/albums/<filename.ext>
    return Path(filename)


class FileModel(models.Model):
    file = models.FileField(blank=False, null=False, upload_to=file_path)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.file.name
