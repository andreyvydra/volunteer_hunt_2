from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from hackaton_test.settings import MAPBOX_ACCESS_TOKEN
from tasks.models import Task
from user.models import Employer


class MapView(LoginRequiredMixin, View):
    template_name = "map/map.html"

    def get(self, request):
        context = dict()
        context["MAPBOX_ACCESS_TOKEN"] = MAPBOX_ACCESS_TOKEN
        employer = Employer.objects.filter(user_id=request.user.id)

        if employer:
            context["tasks"] = Task.objects.\
                values("point_on_map", "category", "name", "id").\
                filter(creator__user_id=request.user.id)
        else:
            context["tasks"] = Task.objects. \
                values("point_on_map", "category", "name", "id").all()

        for task in context["tasks"]:
            task["lon"], task["lat"] = task["point_on_map"].split()

        return render(request, self.template_name, context)

    def post(self, request):
        pass
