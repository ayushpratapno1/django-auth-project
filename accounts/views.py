from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .forms import ProfileForm
from .models import Profile, Message
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


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

@login_required
def dashboard(request):

    if not request.user.is_staff:
        return HttpResponseForbidden(
            "You are not authorized."
        )
    staff_users = User.objects.filter(is_staff=True).count()

    active_users = User.objects.filter(is_active=True).count()

    inactive_users = User.objects.filter(is_active=False).count()

    total_users = User.objects.count()

    total_profiles = Profile.objects.count()

    users = User.objects.all().order_by('-date_joined')

    context = {
    'users': users,
    'total_users': total_users,
    'active_users': active_users,
    'inactive_users': inactive_users,
    'staff_users': staff_users,
    'total_profiles': total_profiles,
    'chart_data': [
        total_users,
        active_users,
        inactive_users,
        staff_users,
        total_profiles
    ]
}

    return render(
        request,
        'dashboard.html',
        context
    )

@login_required
def user_detail(request, user_id):

    if not request.user.is_staff:
        return HttpResponseForbidden()

    selected_user = User.objects.get(
        id=user_id
    )

    return render(
        request,
        'user_detail.html',
        {
            'selected_user': selected_user
        }
    )

@login_required
def members(request):

    members = Profile.objects.select_related(
        "user"
    ).order_by("rank")

    return render(
        request,
        "members.html",
        {
            "members": members
        }
    )

@login_required
def chat(request):

    if request.method == "POST":

        content = request.POST.get(
            "content"
        )

        if content:

            Message.objects.create(
                user=request.user,
                content=content
            )

            return redirect("chat")

    messages = Message.objects.filter(
        is_deleted=False
    ).select_related(
        "user"
    ).order_by(
        "-created_at"
    )[:100]

    messages = reversed(messages)

    return render(
    request,
    "chat.html",
    {
        "messages": messages,
        "message_count": Message.objects.filter(
            is_deleted=False
        ).count()
    }
)