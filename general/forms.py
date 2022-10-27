from django import forms

from general.models import Subscriber


class SubscriberForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Your Email'}))

    class Meta:
        model = Subscriber
        fields = ['email']