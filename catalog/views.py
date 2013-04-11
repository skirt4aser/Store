# -*- coding: utf-8 -*-
from math import *
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from catalog.forms import SupplierForm


@login_required()
def supplier(request):
    # if in a postback
    if request.method == 'POST':
        # getting form
        form = SupplierForm(request.POST)
        # validating form elements
        if form.is_valid():
            # creating and instance of a binded model object
            supplier = form.save(commit=False)
            # populating with form data
            supplier.name = form.cleaned_data['name']
            supplier.address = form.cleaned_data['address']
            supplier.phone = form.cleaned_data['phone']
            supplier.contact = form.cleaned_data['contact']
            supplier.contact_phone = form.cleaned_data['contact_phone']
            supplier.comment = form.cleaned_data['comment']
            supplier.contact_comment = form.cleaned_data['contact_comment']
            # saving to db
            supplier = form.save()
            # redirecting...
            return HttpResponseRedirect('/supplier/')
    else:
        form = SupplierForm()

    return render_to_response('catalog/supplier.html', {'form': form}, RequestContext(request))
