from django.urls import path
from . import views
from .views import home, signup, user_login, user_logout, profile, edit_profile, dashboard, user_detail, members

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/user/<int:user_id>/', user_detail, name='user_detail'),
    path("members/",views.members,name="members")
]