from django.shortcuts import render
from django.views import View

from tasks.models import Task
from user.models import Volunteer, Employer


class HomepageView(View):
    template_name = 'homepage/homepage.html'

    def get(self, request):
        context = dict()
        context['count_volunteers'] = Volunteer.objects.values_list('id', flat=True).all().count()
        context['count_employers'] = Employer.objects.values_list('id', flat=True).all().count()
        context['most_popular_event'] = Task.objects.order_by('-volunteers').all()[0]
        context['most_valuable_employer'] = Employer.objects.order_by('-my_tasks').all()[0]
        context['biggest_number_of_tasks_employer'] = len(context['most_valuable_employer'].my_tasks.all())
        # context['biggest_number_of_tasks_volunteer'] = Task.objects.order
        return render(request, HomepageView.template_name, context=context)
