# myapp/forms.py

from django import forms

class ScheduleForm(forms.Form):
    url = forms.URLField(label='URL', widget=forms.URLInput(attrs={'class': 'form-control', 'required': True}))
    schedule_date = forms.DateField(
        label='Schedule Date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True})
    )
    schedule_time = forms.TimeField(
        label='Schedule Time',
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'required': True})
    )
    output_format = forms.ChoiceField(
        label='Output Format',
        choices=[('pdf', 'PDF'), ('csv', 'CSV'), ('json', 'JSON')],
        widget=forms.Select(attrs={'class': 'form-select', 'required': True})
    )
