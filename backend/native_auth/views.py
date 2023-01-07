from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
import email
from django.shortcuts import render, redirect
from .forms import ProfileEditForm, UserCreationForm, LoginForm
from .models import MyUser, Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def landing_page(request):
    template_name = 'native_auth/landing_page.html'
    context = {'title':'tarsk'}
    if request.user.is_authenticated:
        return redirect('task:dashboard')
    return render(request,template_name,context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print(f'created user: {user} \n current user: {request.user}')
            return redirect('native_auth:edit_profile')
    else:
        form = UserCreationForm()
    return render(request, 'native_auth/signup.html', {'signup_form': form,'title':'dashboard'})

def login_view(request,backend = 'django.contrib.auth.backends.ModelBackend'):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                user.profile.online = True
                user.profile.save()
                messages.info(request, "login successful!")
                if user.profile.first_name == None:
                    return redirect('native_auth:edit_profile')
                if 'user_settings' in request.POST:
                    return redirect('native_auth:settings')
                # messages.info(request, "login successful!")
                return redirect ('task:dashboard')
            else:
                messages.info(request, "login failed!")  
            return redirect('native_auth:landing_page') 
    return render(request, 'native_auth/login.html', context={'form': LoginForm,'title':'login'})


def edit_profile(request):
    form = ProfileEditForm(request.POST or None, instance=request.user.profile)
    from_signup = False
    if request.user.profile.first_name == None:
        from_signup = True
    if request.POST:    
        if form.is_valid():
            profile = form
            profile.save()
            messages.info(request, "profile information updated")
            return redirect('task:dashboard')
            
        else:
            messages.info(request, "please check provided information")
    template_name = 'native_auth/edit_profile.html'
    context = {'form':form}
    return render(request,template_name,context)

@login_required(login_url='landing_page')
def settings(request,slug=email):
    user = request.user
    form = ProfileEditForm(request.POST or None, instance=user.profile)
    template_name = 'native_auth/settings.html'
    context = {'title':f'{user.profile.first_name} | profile', 'user':user, 'form':form}
    return render(request,template_name,context)

@login_required(login_url='landing_page')         
def logout_view(request):
    request.user.profile.online=False
    request.user.profile.save()
    logout(request)
    return redirect('landing_page')

@login_required(login_url='landing_page')
def delete_native_auth(request):
    if request.user.is_authenticated:
        user = request.user
        user.delete()
        return redirect('landing_page')