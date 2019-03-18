# Django Sitemap
Sitemap is a file with an xml extension that contains the pages
of the content we have published on our site.
Today, the site map has become one of the most important SEO criteria
to be found on every site.

We want to start by creating a new project.

```bash
$ django-admin startproject django_sitemap
$ cd django_sitemap/
```

We now want to create a new app and I will call it my app.

```bash
$ ./manage.py startapp myapp
```

we can add `myapp` to our install apps.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]
```

`django_sitemap/urls.py:`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('myapp.urls')),
    path('admin/', admin.site.urls),
]
```

`myapp/urls.py:`

```python
from django.urls import path
from myapp.views import about

urlpatterns = [
    path('about/', about, name='about')
]
```

`myapp/views.py:`

```python
from django.http import HttpResponse

def about(request):
    return HttpResponse('about page')
```

There's a package called `Django contrib sitemaps` 
and start creating our sitemap.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'django.contrib.sitemaps',
]
```

`StaticViewSitemap()` will be a site map for all of our static views.
Every single site map has to have a function called an item and `location()` 
should return a path for every single item.

`myapp/sitemaps.py:`

```python
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['about']

    def location(self, item):
        return reverse(item)

```

We want to import `static view the site map` and then we can create a new dict called
`site maps` and we want to give it the key of `static` and the value of `static view side map`
because we'll need to pass this dict in a moment.


`django_sitemap/urls.py:`

```python
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from myapp.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap
}
urlpatterns = [
    path('', include('myapp.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('admin/', admin.site.urls),
]
```
#### Running the application

```bash
$ python manage.py runserver
```

- `http://127.0.0.1:8000/sitemap.xml`, we get an XML file which contains a location.

```bash
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>http://127.0.0.1:8000/about/</loc>
    </url>
</urlset>
```


## Model

We create a snippet model.

```python
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

```

Using `save()` method. Because, we want to generate the slug from the title.

```bash
$ ./manage.py makemigrations
$ ./manage.py migrate
```

```bash
$ ./manage.py shell
In [1]: from myapp.models import Snippet
In [2]: Snippet.objects.create(title='t1', body='<h1></h1').save()
In [3]: Snippet.objects.create(title='t2', body='<h2></h2').save()    
```

Now, we want to create a real path and our detail views and this one is going to 
take a a slug.

`myapp/urls.py:`

```python
from django.urls import path

from myapp.views import about, snippet_detail

urlpatterns = [
    path('<slug:slug>/', snippet_detail),
    path('about/', about, name='about'),
]

```

`myapp/views.py:`

```python
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Snippet


def about(request):
    return HttpResponse('about page')


def snippet_detail(request, slug):
    snippet = get_object_or_404(Snippet, slug=slug)
    return HttpResponse(f'the detailview for slug of {slug}')

```

#### Running the application

```bash
$ python manage.py runserver
```

- `http://127.0.0.1:8000/h2/`, the detailview for slug of h2.



`django_sitemap/urls.py:`

```python
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from myapp.sitemaps import SnippetSitemap, StaticViewSitemap

sitemaps = {'static': StaticViewSitemap, 'snippet': SnippetSitemap}
urlpatterns = [
    path('', include('myapp.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('admin/', admin.site.urls),
]
```

`myapp/sitemaps.py:`

```python
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

```

#### Running the application

```bash
$ python manage.py runserver
```

- `http://127.0.0.1:8000/sitemap.xml`, we get an XML file which contains a location.

```bash
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>http://127.0.0.1:8000/about/</loc>
    </url>
    <url>
        <loc>http://127.0.0.1:8000/h1</loc>
    </url>
    <url>
        <loc>http://127.0.0.1:8000/h2</loc>
    </url>
    <url>
        <loc>http://127.0.0.1:8000/h3</loc>
    </url>
</urlset>
```

## Conclusion
if you look in the [django site maps documentation](https://docs.djangoproject.com/en/2.1/ref/contrib/sitemaps/).
You will find other properties which can use
on the site map to tell search engines more about it.
In this article you’ve learned how to create a site map.
