from django import forms
from .models import Robot


class RobotCreationForm(forms.ModelForm):
    '''Validation for Robot model'''
    class Meta:
        model = Robot
        fields = ['serial', 'model', 'version', 'created']
