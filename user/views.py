from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View

from user.models import User, Volunteer

import django.contrib.auth.views as admin_views

from user.forms import RegistrationForm


class ProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        context = {
            'user': user
        }
        try:
            volunteer = Volunteer.objects.get(user=user)
            context['task'] = volunteer.task
        except Volunteer.DoesNotExist:
            pass
        return render(request, self.template_name, context)


class SignupView(View):
    template_name = 'users/auth/signup.html'

    def get(self, request):
        form = RegistrationForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            return redirect('login')
        else:
            context = {'form': form}
            return render(request, self.template_name, context)


@login_required
def get_user_profile(request, pk):
    # я переписал чуть выше
    user = User.objects.get(pk=pk)
    return render(request, 'users/profile.html', {'user': user})


# Django auth views
class LoginView(admin_views.LoginView):
    template_name = 'users/auth/login.html'


class PasswordChangeDoneView(admin_views.PasswordChangeDoneView):
    template_name = 'users/auth/password_change_done.html'


class LogoutView(admin_views.LogoutView):
    template_name = 'users/auth/logout.html'


class PasswordResetView(admin_views.PasswordResetView):
    template_name = 'users/auth/password_reset.html'


class PasswordResetDoneView(admin_views.PasswordResetDoneView):
    template_name = 'users/auth/password_reset_done.html'


class PasswordResetConfirmView(admin_views.PasswordResetConfirmView):
    template_name = 'users/auth/reset.html'


class PasswordResetCompleteView(admin_views.PasswordResetCompleteView):
    template_name = 'users/auth/reset_done.html'


class PasswordChangeView(admin_views.PasswordChangeView):
    template_name = 'users/auth/password_change.html'
