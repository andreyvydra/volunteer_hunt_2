import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, UpdateView

from hackaton_test.settings import MAPBOX_ACCESS_TOKEN
from tasks.forms import TaskForm, UpdateTaskForm
from tasks.models import Task
from user.models import Employer, Volunteer, User


class TaskView(LoginRequiredMixin, View):
    template_name = 'task/index.html'
    success_url = reverse_lazy('map')

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['pk'])
        employer = Employer.objects.filter(user_id=request.user.id)
        volunteer = Volunteer.objects.filter(user_id=request.user.id)
        context = {
            'task': task,
            'is_employer': bool(employer),
            'is_volunteer': bool(volunteer),
            'is_active_task': task.datetime >= timezone.now(),
            'belongs_to_user': task.creator.user_id == request.user.id,
        }

        volunteers_values_list = task.volunteers.values_list('user_id', flat=True).all()
        context['volunteers_number'] = len(volunteers_values_list)
        if request.user.id in volunteers_values_list:
            context['volunteer_on_task'] = True
        if len(volunteers_values_list) < task.max_volunteer:
            context['volunteer_not_enough'] = True

        context['MAPBOX_ACCESS_TOKEN'] = MAPBOX_ACCESS_TOKEN
        context['task_lon'], context['task_lat'] = task.point_on_map.split()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['pk'])
        if 'task_delete' in request.POST:
            task.delete()
        elif 'task_update' in request.POST:
            return redirect(reverse_lazy('task_update', kwargs=kwargs))
        elif 'task_join' in request.POST:
            user = User.objects.get(pk=request.user.id)
            task.volunteers.add(user.volunteer)
            task.save()
        elif 'task_leave' in request.POST:
            user = User.objects.get(pk=request.user.id)
            task.volunteers.remove(user.volunteer)
            task.save()

        return redirect(TaskView.success_url)


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    form_class = UpdateTaskForm
    model = Task
    template_name = "task/create_update_task.html"
    success_url = reverse_lazy('map')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        employer = Employer.objects.filter(user_id=request.user.id)
        if not employer:
            return HttpResponseNotFound('Задача не была найдена')
        if employer[0].id != self.object.creator.id:
            return HttpResponseNotFound('Задача не была найдена')
        if self.object.datetime.timestamp() < datetime.datetime.now().timestamp():
            return HttpResponseNotFound('Задача уже была завершена')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MAPBOX_ACCESS_TOKEN'] = MAPBOX_ACCESS_TOKEN
        context['lon'], context['lat'] = self.object.point_on_map.split()
        context['color'] = self.object.category.color
        return context


class CreateTaskView(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = "task/create_update_task.html"

    def dispatch(self, request, *args, **kwargs):
        employer = Employer.objects.filter(user_id=request.user.id)
        if not employer:
            return HttpResponseNotFound('Задача не была найдена')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MAPBOX_ACCESS_TOKEN'] = MAPBOX_ACCESS_TOKEN
        return context

    def post(self, request, *args, **kwargs):
        form = CreateTaskView.form_class(request.POST or None)
        if form.is_valid():
            task = Task()
            creator = Employer.objects.get(user_id=request.user.id)
            task.creator = creator
            task.name = form.cleaned_data['name']
            task.category = form.cleaned_data['category']
            task.description = form.cleaned_data['description']
            task.datetime = form.cleaned_data['datetime']
            task.settings = form.cleaned_data['settings']
            task.max_volunteer = form.cleaned_data['max_volunteer']
            task.point_on_map = form.cleaned_data['point_on_map']
            task.save()
            return render(request, 'task/successful_create_task.html', context={"task_id": task.id})
        return redirect(reverse_lazy('map'))
