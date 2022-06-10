from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from tasks.models import Task
from user.models import Employer


class TaskView(LoginRequiredMixin, View):
    template_name = 'task/index.html'
    success_url = reverse_lazy('map')

    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        employer = Employer.objects.filter(user_id=request.user.id)
        context = {
            'task': task,
            'is_employer': bool(employer),
            'belongs_to_user': task.creator.user_id == request.user.id
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if 'task_delete' in request.POST:
            task = Task.objects.get(pk=pk)
            task.delete()
        return redirect(TaskView.success_url)


class DeleteTaskView(DeleteView):
    model = Task
