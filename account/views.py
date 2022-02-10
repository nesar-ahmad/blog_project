from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginForm, RegisterForm, ProfileEditForm, UserEditForm
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.models import User
from .models import Profile
from django.urls import reverse


def user_login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd["username"],
                                password=cd["password"])
            if user is not None:
                # user is authenticated
                if user.is_active:
                    login(request, user)
                    # return HttpResponse('Authenticated successfully')
                    if request.GET.get("next"):
                        return HttpResponseRedirect(request.GET.get("next"))
                    else:
                        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
                else:
                    return HttpResponse('Disabled account')
            else:
                # return HttpResponse("Invalid login")
                context = {'err': 'Invalid username or password.',
                            'form': form}
            return render(request, 'account/login.html', context)
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'account/login.html', context)


def user_logout(request):
    logout(request)
    return render(request, 'account/logout.html')


def profile(request):
    profile = request.user.profile
    return render(request, 'account/profile.html', {"profile": profile})


def register(request):
    # Register a user with its profile fields
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                username=cd["username"],
                first_name=cd["first_name"],
                last_name=cd["last_name"],
                email=cd["email"],
                password=cd["password"]
            )
            user.save()
            
            profile = Profile(
                user=user,
                gender=form.cleaned_data["gender"],
                date_of_birth=form.cleaned_data["date_of_birth"],
                credit=form.cleaned_data["credit"],
                photo=form.cleaned_data["photo"]
            )
            profile.save()
        return render(request, 'account/register_done.html', {'user': user})

    return render(request, 'account/register.html', {'form': form})


def profile_edit(request):
    # Edit a user's profile
    if request.method == 'POST':
        profile_edit_form = ProfileEditForm(request.POST, request.FILES,
                                            instance=request.user.profile)
        user_edit_form = UserEditForm(request.POST, instance=request.user)
        if profile_edit_form.is_valid() and user_edit_form.is_valid():
            profile_edit_form.save()
            user_edit_form.save()
        return HttpResponseRedirect(reverse('account:profile'))
    else:
        profile_edit_form = ProfileEditForm(instance=request.user.profile)
        user_edit_form = UserEditForm(instance=request.user)

    context = {'profile_edit_form': profile_edit_form,
                # 'profile_edit_photo': request.user.profile.photo,
                'user_edit_form': user_edit_form,}

    return render(request, 'account/profile_edit.html', context)
