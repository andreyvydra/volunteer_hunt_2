from django.forms import ModelForm, DateInput, HiddenInput

from hackaton_test.settings import DATE_INPUT_FORMATS
from tasks.models import Task


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['point_on_map'].widget = HiddenInput()

    class Meta:
        model = Task
        fields = ['name', 'description', 'category',
                  'settings', 'datetime',
                  'max_volunteer', 'point_on_map']
        widgets = {
            'datetime': DateInput(
                attrs={
                    'type': 'datetime-local',
                    'step': '1'
                },
            )
        }



class UpdateTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateTaskForm, self).__init__(*args, **kwargs)
        self.initial['datetime'] = self.initial['datetime'].strftime(DATE_INPUT_FORMATS[0])
        self.fields['point_on_map'].widget = HiddenInput()

    class Meta:
        model = Task
        fields = ['name', 'description', 'category',
                  'settings', 'datetime',
                  'max_volunteer', 'point_on_map']
        widgets = {
            'datetime': DateInput(
                attrs={
                    'type': 'datetime-local',
                    'step': '1'
                },
            )
        }
