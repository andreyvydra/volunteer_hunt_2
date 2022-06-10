from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from hackaton_test.settings import MAPBOX_ACCESS_TOKEN
from tasks.models import Task


class MapView(View, LoginRequiredMixin):
    template_name = "map/map.html"

    def get(self, request):
        context = dict()
        context["MAPBOX_ACCESS_TOKEN"] = MAPBOX_ACCESS_TOKEN
        context["tasks"] = Task.objects.values("point_on_map", "category", "name", "id").filter(creator_id=request.user.id)
        for task in context["tasks"]:
            task["lon"], task["lat"] = task["point_on_map"].split()
        return render(request, self.template_name, context)
