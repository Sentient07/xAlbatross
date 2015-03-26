__author__ = 'ramana'
from django import forms
from book.models import ModeofTransport


class BookingForm(forms.ModelForm):
    source_location = forms.CharField(label="Source Location", max_length=30,
                                      widget=forms.TextInput(attrs={
                                          'placeholder': 'Source'}),
                                      required=True,
                                      error_messages={
                                          'required': 'Please enter an EmailID.'})
    destination_location = forms.CharField(label="Destination",
                                           widget=forms.TextInput(attrs={
                                               'placeholder': 'Destination'}),
                                           required=True,
                                           error_messages={
                                               'required': 'Please enter a Destination.'})

    journey_date = forms.CharField(label="Date",
                                   widget=forms.DateInput(attrs={
                                       'placeholder': 'Destination'}),
                                   required=True,
                                   error_messages={
                                       'required': 'Please Choose a Date of journey.'})
    number_of_tickets = forms.IntegerField(label="Date",
                                           widget=forms.CheckboxInput(attrs={
                                               'placeholder': 'Number of tickets'}),
                                           required=True,
                                           error_messages={
                                               'required': 'Please enter the number of tickets.'})
    mode_of_transport = forms.ModelChoiceField(queryset=ModeofTransport.objects.all())

    class Meta:
        pass

    def save(self, commit=True):
        super(BookingForm, self).save(commit=False)
        source_location = self.cleaned_data['source_location']
        destination_location = self.cleaned_data['destination_location']
        if not source_location == destination_location:
            super(BookingForm, self).save(commit=True)
