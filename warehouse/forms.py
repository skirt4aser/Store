from django.forms import ModelForm
from django.forms.widgets import Textarea, Select
from database.models import Purchase, ProductOfPurchase, Acceptance, ReturnModel, WriteOff, ProductAtWarehouse, DishOfWarehouse
from django import forms

__author__ = 'Ars'

class PurchaseForm(ModelForm):

    class Meta:
        model = Purchase
        exclude = ('author','created','modified_date','modified_author')
        widgets = {
            'comment'   :   Textarea(attrs={'rows':'5', 'cols':'3'})
        }

class ProductOfPurchaseForm(ModelForm):
    purchase_amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    class Meta:
        model = ProductOfPurchase
        exclude = ('purchase')
        widgets = {
            'product'           :   Select(attrs={'style':'width:220px;'}),
        }

class AcceptanceForm(ModelForm):

    class Meta:
        model = Acceptance
        exclude = ('author','created','modified_date','modified_author','purchase')
        widgets = {
            'comment'   :   Textarea(attrs={'rows':'5', 'cols':'3'}),
        }

class ReturnForm(ModelForm):

    class Meta:
        model = ReturnModel
        exclude = ('author','created','modified_date','modified_author','acceptance')
        widgets = {
            'comment'   :   Textarea(attrs={'rows':'5', 'cols':'3'}),
            }

class WriteOffForm(ModelForm):

    class Meta:
        model = WriteOff
        exclude = ('author','created','modified_date','modified_author')
        widgets = {
            'comment'   :   Textarea(attrs={'rows':'5', 'cols':'3'})
        }

class ProductAtWarehouseForm(ModelForm):
    class Meta:
        model = ProductAtWarehouse
        widgets = {
            'product'           :   Select(attrs={'style':'width:220px;'}),
            }

class DishOfWarehouseForm(ModelForm):
    class Meta:
        model = DishOfWarehouse
        widgets = {
            'dish'           :   Select(attrs={'style':'width:220px;'}),
            }
