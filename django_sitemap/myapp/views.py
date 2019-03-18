from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Snippet


def about(request):
    return HttpResponse('about page')


def snippet_detail(request, slug):
    snippet = get_object_or_404(Snippet, slug=slug)
    return HttpResponse(f'the detailview for slug of {slug}')
