from django import forms
from database.models import Supplier

#from bootstrap_toolkit.widgets import BootstrapTextInput, BootstrapUneditableInput, BootstrapDateInput


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
