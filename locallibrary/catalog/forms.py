import datetime
from django import forms
from catalog.models import BookInstance
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _



class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4weeks(default='3weeks')")

    def clean_renewal_date(self):
        data = self.cleaned_data["renewal_date"]
        
        #check if a date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_("invalid date - renewal in past"))

        if data> datetime.date.today() + datetime.timedelta(weeks=4):
            raise validationError(_("Invalid date - renewal date more than 4 weeks"))

        #remember to always return the cleaned data
        return data
    
#using the model form instead
class RenewBookModelForm(ModelForm):

    def clean_due_back(self):
        data = self.cleaned_data["renewal_date"]
        
        #check if a date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_("invalid date - renewal in past"))

        if data> datetime.date.today() + datetime.timedelta(weeks=4):
            raise validationError(_("Invalid date - renewal date more than 4 weeks"))

        #remember to always return the cleaned data
        return data

    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('New renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}