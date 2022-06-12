import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View

from user.models import User, Volunteer, Employer

import django.contrib.auth.views as admin_views

from user.forms import RegistrationForm


class ProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request):
        user = request.user
        context = {
            'user': user
        }
        try:
            volunteer = Volunteer.objects.get(user=user)
            context['active_tasks'] = volunteer.task.filter(datetime__gte=timezone.now())
            context['not_active_tasks'] = volunteer.task.filter(datetime__lt=timezone.now())
        except Volunteer.DoesNotExist:
            employer = Employer.objects.get(user=user)
            context['active_tasks'] = employer.my_tasks.filter(datetime__gte=timezone.now())
            context['not_active_tasks'] = employer.my_tasks.filter(datetime__lt=timezone.now())
        return render(request, self.template_name, context)


class SignupView(View):
    template_name = 'users/auth/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('homepage'))
        return super().dispatch(request, *args, **kwargs)

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
            if request.POST['user_type'] == "1":
                new_volunteer = Volunteer()
                new_volunteer.user = new_user
                new_volunteer.level = 1
                new_volunteer.save()
            else:
                new_employer = Employer()
                new_employer.user = new_user
                new_employer.save()
            return redirect('login')
        else:
            context = {'form': form}
            return render(request, self.template_name, context)


# Django auth views
class LoginView(admin_views.LoginView):
    template_name = 'users/auth/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('homepage'))
        return super().dispatch(request, *args, **kwargs)


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
