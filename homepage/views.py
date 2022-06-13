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
        context['most_popular_event'] = Task.objects.order_by('-volunteers').all()
        if context['most_popular_event']:
            context['most_popular_event'] = context['most_popular_event'][0]
        else:
            context['most_popular_event'] = None
        context['most_valuable_employer'] = Employer.objects.order_by('-my_tasks').all()
        if context['most_valuable_employer']:
            context['most_valuable_employer'] = context['most_valuable_employer'][0]
        else:
            context['most_valuable_employer'] = None
        context['biggest_number_of_tasks_employer'] = len(context['most_valuable_employer'].my_tasks.all())
        return render(request, HomepageView.template_name, context=context)
