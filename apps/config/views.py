from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render 

from apps.config.models import Shortener
from apps.config.forms import ShortenerForm

# Create your views here.


@login_required(login_url='login')
def home(request):
    context = {}
    context['form'] = ShortenerForm()
    if request.method == 'GET':
        return render(request, 'urlshortener/home.html', context)
    elif request.method == 'POST':
        used_form = ShortenerForm(request.POST)
        if used_form.is_valid():
            shortened_object = used_form.save()
            shortened_object = used_form.save()
            shortened_object.user = request.user
            shortened_object.save()
            new_url = request.build_absolute_uri('/') + shortened_object.short_url
            long_url = shortened_object.long_url 
            context['new_url']  = new_url
            context['long_url'] = long_url
            return render(request, 'urlshortener/home.html', context)
        context['errors'] = used_form.errors
        return render(request, 'urlshortener/home.html', context)

@login_required(login_url='login')
def user_links(request):
    all_urls = None
    
    if Shortener.objects.filter(user=request.user).exists():
        all_urls = Shortener.objects.filter(user=request.user)
    current_site = get_current_site(request)
    return render(request, 'urlshortener/user_urls.html', context={'domain': current_site, 'all_urls': all_urls})

@login_required(login_url='login')
def delete(request,pk):
    if request.POST:
        url = Shortener.objects.get(pk=pk)
        if url.user == request.user:
            url.delete()
    return JsonResponse({"passed": True,})

@login_required(login_url='login')
def redirect_url_view(request, shortened_part):
    try:
        shortener = Shortener.objects.get(short_url=shortened_part)
        shortener.times_followed += 1        
        shortener.save()
        return HttpResponseRedirect(shortener.long_url)     
    except:
        raise Http404('Sorry this link is broken :(')