from django.shortcuts import render
from django.views import View


class HomepageView(View):
    template_name = 'homepage/homepage.html'

    def get(self, request):
        return render(request, HomepageView.template_name)