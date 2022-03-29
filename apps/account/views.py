from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse


from apps.account.models import Account, UserConfirmCode
from apps.account.utils import generate_token, create_random_code
from apps.account.tasks import send_email_on_registration, send_email_on_login
from apps.account.forms import RegistrationForm, UserForm, LoginConfirmForm


def log_user_in(request):
    error_messages = None
    if request.method == "POST":
        form = UserForm(data=request.POST)
        if form.is_valid():
            email  = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                code = create_random_code()
                UserConfirmCode.objects.create(user=user, code=code)
                current_site = get_current_site(request)
                send_email_on_login(current_site.domain, user.id, code)
                return redirect("login-confirm", pk=user.pk)
            else:
                error_messages = "Invalid email or password. If all correct Check your email to verify account "
        else:
            error_messages = "Invalid email or password."
    else:
        form = UserForm(data=request.POST)
    return render(request, 'accounts/login.html', context={'form':form, 'error_message': error_messages})


def log_user_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

  
def register(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next') or 'homepage'
        return redirect(next_url)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            send_email_on_registration(current_site.domain, user.id)
            return redirect('login')
        else:
            return HttpResponse(status=400)
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', context={'form': form, 'next': request.GET.get('next') or 'homepage'})


def activate_user(request, uid, token):
    user = Account.objects.filter(id=uid).first()
    if user:
        if generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect(reverse('homepage'))
    return HttpResponse(content='Invalid activation link', status=401)


def login_confirm(request, pk):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        form = LoginConfirmForm(request.POST)
        if form.is_valid():
            user =  Account.objects.get(pk=pk)
            if UserConfirmCode.objects.filter(user=user, code=request.POST['code']).exists():
                login(request,user)
                UserConfirmCode.objects.filter(user=user, code=request.POST['code']).delete()
                return redirect('homepage')
    else:
        form = LoginConfirmForm()
    return render(request, 'accounts/login_confirm.html', context={'form': form , 'pk': pk})