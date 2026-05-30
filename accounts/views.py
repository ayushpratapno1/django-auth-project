from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .forms import ProfileForm


# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):

    if request.method == 'POST':

        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            messages.error(
                request,
                'Invalid username or password'
            )

    return render(request, 'login.html')

def user_logout(request):

    logout(request)

    return redirect('home')

@login_required
def profile(request):

    return render(
        request,
        'profile.html'
    )

@login_required
def edit_profile(request):

    profile = request.user.profile

    if request.method == 'POST':

        form = ProfileForm(
    request.POST,
    request.FILES,
    instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect('profile')

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'edit_profile.html',
        {
            'form': form
        }
    )