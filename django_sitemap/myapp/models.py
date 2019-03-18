from django.db import models
from django.utils.text import slugify


class Snippet(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(blank=True, null=True)
    body = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/{self.slug}'
