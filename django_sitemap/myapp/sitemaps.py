from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from .models import Snippet


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['about']

    def location(self, item):
        return reverse(item)


class SnippetSitemap(Sitemap):
    def items(self):
        return Snippet.objects.all()
