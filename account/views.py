from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from account.form import LoginForm, RegisterUserForm, ProfileForm


def user_login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                print(user.is_active)
                if user.is_active:
                    login(request, user)
                    return HttpResponse('auth succc')
                else:
                    return HttpResponse('Disable account')
            else:
                return HttpResponse('invalid login')
        return render(request, 'auth/login.html', {'form', form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html')


def user_register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

        else:
            pass

        return render(request, 'auth/register.html', {'form': form})
    else:
        form = RegisterUserForm()
        return render(request, 'auth/register.html', {'form': form})


def user_profile(request):
    if request.method=='POST':
        profile_form=ProfileForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        profile_form.save(commit=True)
    else:
        profile_form = ProfileForm(
            instance=request.user.profile)

    return render(request, 'auth/profile.html', {'form': profile_form})
