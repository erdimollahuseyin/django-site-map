from django.urls import path

from myapp.views import about, snippet_detail

urlpatterns = [
    path('<slug:slug>/', snippet_detail),
    path('about/', about, name='about'),
]
