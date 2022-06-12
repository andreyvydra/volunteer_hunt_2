from django.shortcuts import render
from django.views import View

from user.models import Volunteer, Employer


class HomepageView(View):
    template_name = 'homepage/homepage.html'

    def get(self, request):
        context = dict()
        context['count_volunteers'] = Volunteer.objects.values_list('id', flat=True).all().count()
        context['count_employers'] = Employer.objects.values_list('id', flat=True).all().count()
        return render(request, HomepageView.template_name, context=context)
