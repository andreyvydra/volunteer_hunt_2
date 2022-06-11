from django.db import models


class TaskManager(models.Manager):
    def get_tasks_from_context(self, context: dict):
        obj_to_return = self

        category = context.get('category')
        from_date = context.get('from_date')
        to_date = context.get('to_date')

        if category:
            obj_to_return = obj_to_return.filter(category__name__iexact=category)

        if from_date:
            obj_to_return = obj_to_return.filter(datetime__gte=from_date)

        if to_date:
            obj_to_return = obj_to_return.filter(datetime__lte=to_date)

        return obj_to_return
