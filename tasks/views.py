from django.shortcuts import render
from django.views import View
from tasks.models import Task


class TaskView(View):
    template_name = 'task/index.html'

    def get(self, pk, request):
        task = Task.objects.get(pk=pk)
        context = {
            'task': task
        }
        print(1)
        return render(request, self.template_name, context)
