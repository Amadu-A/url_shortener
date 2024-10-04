from django.shortcuts import render, redirect
from .models import ShortenedURL
from .forms import URLForm
from .utils import generate_short_code

# Вьюшка для создания новой ссылки
def create_short_url(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            shortened_url = form.save(commit=False)
            shortened_url.short_code = generate_short_code()
            shortened_url.save()
            return redirect('url_list')  # Переход на страницу списка ссылок
    else:
        form = URLForm()
    return render(request, 'shortener/create_short_url.html', {'form': form})

# Вьюшка для просмотра списка ссылок
def url_list(request):
    urls = ShortenedURL.objects.all()
    return render(request, 'shortener/url_list.html', {'urls': urls})