from django.contrib.auth.decorators import login_required
from django.urls import path
from user import views


urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),

    path('profile/', login_required(views.ProfileView.as_view()), name='users-profile'),

    # Django login
    path(
        'login/',
        views.LoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'password_change/',
        views.PasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        'password_change/done/',
        views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),

    path(
        'password_reset/',
        views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
]
