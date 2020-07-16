from django.db import models


class Core(models.Model):

    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    date_modif = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f'{self.title}' if self.title else ''

    # def delete(self, **kwargs):
    #     if 'force' in kwargs:
    #         super().delete()
    #     else:
    #         self.active = False
    #         self.save()


class Article(Core):
    pass

