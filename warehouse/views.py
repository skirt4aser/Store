# -*- coding: utf-8 -*-
import datetime
from math import *
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from database.models import Purchase, ProductOfPurchase, Acceptance, ProductAtWarehouse, ReturnModel
from warehouse.forms import PurchaseForm, ProductOfPurchaseForm, AcceptanceForm, ReturnForm

__author__ = 'Ars'

@login_required()
def purchases(request, page_pk):
    page_pk = int(page_pk)
    per_page = 10
    purchases = Purchase.objects.all().order_by('date_purchase','pk')
    all = purchases.count()
    pages = int(ceil(all/float(per_page)))
    if page_pk>pages and page_pk!=1:
        raise  Http404()
    page_list = []
    for i in range(pages):
        page_list.append(i+1)
    prev = 1
    if page_pk!=1:
        prev = page_pk -1
    if page_pk==pages:
        next = page_pk
    else:
        next = page_pk + 1
    range_date = request.POST.get('report_range', '')
    if range_date!='':
        start = range_date[:10]
        end = range_date[14:]
        try:
            purchases = purchases.filter(date_purchase__gte=start, date_purchase__lte=end)
        except :
            print 'bad date request'
    purchases = purchases[per_page*page_pk-per_page:per_page*page_pk]
    purchase_list = []
    for purchase in purchases:
        sum = 0
        for product in purchase.productofpurchase_set.all():
            sum += product.purchase_amount * product.purchase_price
        purchase_list.append([purchase, sum])
    return render_to_response('warehouse/purchases.html',{'purchases'   :   purchase_list,
                                                          'range'       :   range_date,
                                                          'pages'       :   page_list,
                                                          'current'     :   page_pk,
                                                          'prev'        :   prev,
                                                          'next'        :   next
                                                          }, RequestContext(request))

@login_required()
def purchase(request, id_purchase):
    product_list = []
    total = 0
    purchase = ''
    if not id_purchase:
        form_purchase = PurchaseForm(request.POST or None)
        form_product = ProductOfPurchaseForm(request.POST or None)
        if request.method == 'POST' and form_purchase.is_valid() and form_product.is_valid():
            purchase = form_purchase.save(commit=False)
            purchase.created = datetime.date.today()
            purchase.author = request.user
            purchase.modified_date = datetime.date.today()
            purchase.modified_author = request.user
            purchase.save()
            product = form_product.save(commit=False)
            product.purchase = purchase
            product.save()
            return HttpResponseRedirect('/purchase/'+str(purchase.pk))
    else:
        purchase = get_object_or_404(Purchase, pk=id_purchase)
        issued = purchase.issued
        products = purchase.productofpurchase_set.all().order_by('pk')
        for product in products:
            total += product.purchase_amount * product.purchase_price
            product_list.append([product, product.purchase_amount * product.purchase_price])
        form_purchase = PurchaseForm(request.POST or None, instance=purchase)
        form_product = ProductOfPurchaseForm(request.POST or None)
        if request.method == 'POST' and form_purchase.is_valid() and form_product.is_valid():
            purchase = form_purchase.save(commit=False)
            purchase.modified_date = datetime.date.today()
            purchase.modified_author = request.user
            purchase.issued = issued
            purchase.save()
            product = form_product.save(commit=False)
            product.purchase = purchase
            product.save()
            return HttpResponseRedirect('/purchase/'+str(purchase.pk))
    return render_to_response('warehouse/purchase.html',{'form_purchase'    :   form_purchase,
                                                         'form_product'     :   form_product,
                                                         'products'         :   product_list,
                                                         'total'            :   total,
                                                         'id_purchase'      :   id_purchase,
                                                         'purchase'         :   purchase
    }, RequestContext(request))

@login_required()
def purchase_product(request, id_purchase, id_product):
    product_list = []
    total = 0
    purchase = get_object_or_404(Purchase, pk=id_purchase)
    product = get_object_or_404(ProductOfPurchase, pk=id_product)
    issued = purchase.issued
    products = purchase.productofpurchase_set.all().order_by('pk')
    for prod in products:
        total += prod.purchase_amount * prod.purchase_price
        product_list.append([prod, prod.purchase_amount * prod.purchase_price])
    form_purchase = PurchaseForm(request.POST or None, instance=purchase)
    form_product = ProductOfPurchaseForm(request.POST or None, instance=product)
    if request.method == 'POST' and form_purchase.is_valid() and form_product.is_valid():
        purchase = form_purchase.save(commit=False)
        purchase.modified_date = datetime.date.today()
        purchase.modified_author = request.user
        purchase.issued = issued
        purchase.save()
        form_product.save()
        return HttpResponseRedirect('/purchase/'+str(purchase.pk))
    return render_to_response('warehouse/purchase.html',{'form_purchase'    :   form_purchase,
                                                         'form_product'     :   form_product,
                                                         'products'         :   product_list,
                                                         'total'            :   total,
                                                         'id_purchase'      :   id_purchase
    }, RequestContext(request))

@login_required()
def purchase_product_delete(request, id_product):
    product = get_object_or_404(ProductOfPurchase, pk=id_product)
    purchase_pk = product.purchase.pk
    product.delete()
    return HttpResponseRedirect('/purchase/'+str(purchase_pk))

@login_required()
def purchase_delete(request, id_purchase):
    purchase = get_object_or_404(Purchase, pk=id_purchase)
    purchase.delete()
    return HttpResponseRedirect('/purchases/page/1/')





@login_required()
def acceptance(request, id_purchase):
    purchase = get_object_or_404(Purchase, pk=id_purchase)
    product_list = []
    old_product_list = []
    try:
        form_acceptance = AcceptanceForm(request.POST or None, instance=purchase.acceptance)
        exist = True
        for product in purchase.productofpurchase_set.all():
            old_product_list.append(product)
    except :
        form_acceptance = AcceptanceForm(request.POST or None)
        exist = False
    AcceptanceInlineFormSet = inlineformset_factory(Purchase,ProductOfPurchase, max_num=purchase.productofpurchase_set.all().count(), fields=('acceptance_amount','acceptance_price'),can_delete=False,)
    form_products = AcceptanceInlineFormSet(request.POST or None, instance=purchase)
    for i in range(len(form_products)):
        product_list.append([form_products.get_queryset()[i],form_products[i],
                             form_products.get_queryset()[i].purchase_amount * form_products.get_queryset()[i].purchase_price])
    if form_acceptance.is_valid() and form_products.is_valid():
        acceptance = form_acceptance.save(commit=False)
        if not exist:
            acceptance.created = datetime.date.today()
            acceptance.author = request.user
        acceptance.modified_date = datetime.date.today()
        acceptance.modified_author = request.user
        acceptance.purchase = purchase
        acceptance.save()
        form_products.save()

        if exist:
            for old in old_product_list:
                try:
                    prod_war = ProductAtWarehouse.objects.get(product=old.product, warehouse=old.purchase.warehouse, price=old.acceptance_price)
                    prod_war.amount -= old.acceptance_amount
                    prod_war.date = old.purchase.acceptance.date
                    prod_war.save()
                    if not prod_war.amount:
                        prod_war.delete()
                except ProductAtWarehouse.DoesNotExist:
                    ProductAtWarehouse.objects.create(product=old.product, warehouse=old.purchase.warehouse, amount=old.acceptance_amount, price=old.acceptance_price,
                                                                        date=old.purchase.acceptance.date)

        for product in purchase.productofpurchase_set.all():
            try:
                prod_war = ProductAtWarehouse.objects.get(product=product.product, warehouse=product.purchase.warehouse, price=product.acceptance_price)
                prod_war.amount += product.acceptance_amount
                prod_war.date = product.purchase.acceptance.date
                prod_war.save()
                if not prod_war.amount:
                    prod_war.delete()
            except ProductAtWarehouse.DoesNotExist:
                ProductAtWarehouse.objects.create(product=product.product, warehouse=product.purchase.warehouse, amount=product.acceptance_amount, price=product.acceptance_price,
                                                        date=product.purchase.acceptance.date)
        return HttpResponseRedirect('/acceptances/page/1')
    return render_to_response('warehouse/acceptance.html',{'form_acceptance'    :   form_acceptance,
                                                           'purchase'           :   purchase,
                                                           'products'           :   product_list,
                                                           'form_products'      :   form_products
    },RequestContext(request))


@login_required()
def acceptances(request, page_pk):
    page_pk = int(page_pk)
    per_page = 10
    acceptances = Acceptance.objects.all().order_by('date','pk')
    all = acceptances.count()
    pages = int(ceil(all/float(per_page)))
    if page_pk>pages and page_pk!=1:
        raise  Http404()
    page_list = []
    for i in range(pages):
        page_list.append(i+1)
    prev = 1
    if page_pk!=1:
        prev = page_pk -1
    if page_pk==pages:
        next = page_pk
    else:
        next = page_pk + 1
    range_date = request.POST.get('report_range', '')
    if range_date!='':
        start = range_date[:10]
        end = range_date[14:]
        try:
            acceptances = acceptances.filter(date__gte=start, date__lte=end)
        except :
            print 'bad date request'
    acceptances = acceptances[per_page*page_pk-per_page:per_page*page_pk]
    return render_to_response('warehouse/acceptances.html',{'acceptances' :   acceptances,
                                                          'range'       :   range_date,
                                                          'pages'       :   page_list,
                                                          'current'     :   page_pk,
                                                          'prev'        :   prev,
                                                          'next'        :   next
    }, RequestContext(request))


@login_required()
def return_view(request, id_acceptance):
    acceptance = get_object_or_404(Acceptance, pk=id_acceptance)
    old_product_list = []
    product_list = []
    failure = ''
    try:
        form_return = ReturnForm(request.POST or None, instance=acceptance.returnmodel)
        exist = True
        for product in acceptance.purchase.productofpurchase_set.all():
            old_product_list.append(product)
    except :
        form_return = ReturnForm(request.POST or None)
        exist = False
    AcceptanceInlineFormSet = inlineformset_factory(Purchase,ProductOfPurchase, max_num=acceptance.purchase.productofpurchase_set.all().count(), fields=('return_amount',),can_delete=False,)
    form_products = AcceptanceInlineFormSet(request.POST or None, instance=acceptance.purchase)
    for i in range(len(form_products)):
        product_list.append([form_products.get_queryset()[i],form_products[i],
                             form_products.get_queryset()[i].purchase_amount * form_products.get_queryset()[i].purchase_price])
    if form_return.is_valid() and form_products.is_valid():
        return_m = form_return.save(commit=False)
        if not exist:
            return_m.created = datetime.date.today()
            return_m.author = request.user
        return_m.modified_date = datetime.date.today()
        return_m.modified_author = request.user
        return_m.acceptance = acceptance

        if exist:
            for old in old_product_list:
                try:
                    prod_war = ProductAtWarehouse.objects.get(product=old.product, warehouse=old.purchase.warehouse, price=old.acceptance_price)
                    prod_war.amount += old.return_amount
                    prod_war.save()
                except ProductAtWarehouse.DoesNotExist:
                    ProductAtWarehouse.objects.create(product=old.product,warehouse=old.purchase.warehouse,amount=old.return_amount,price=old.acceptance_price,date=old.purchase.acceptance.date)

        for product in form_products.get_queryset():
            try:
                prod_war = ProductAtWarehouse.objects.get(product=product.product, warehouse=product.purchase.warehouse, price=product.acceptance_price)
                if prod_war.amount - product.return_amount < 0:
                    for old in old_product_list:
                        try:
                            prod_war = ProductAtWarehouse.objects.get(product=old.product, warehouse=old.purchase.warehouse, price=old.acceptance_price)
                            prod_war.amount -= old.return_amount
                            prod_war.save()
                            if not prod_war.amount:
                                prod_war.delete()
                        except ProductAtWarehouse.DoesNotExist:
                            print 'DoesNotExist'
                    failure = u'На складе: ' + prod_war.warehouse.name + u' невозможно сделать возврат по товару: ' + prod_war.product.name + u' , так как его осталось ' + str(prod_war.amount)
                    return render_to_response('warehouse/return.html',{'form_return'        :   form_return,
                                                                       'acceptance'         :   acceptance,
                                                                       'products'           :   product_list,
                                                                       'form_products'      :   form_products,
                                                                       'failure'            :   failure
                    },RequestContext(request))
            except ProductAtWarehouse.DoesNotExist:
                for old in old_product_list:
                    try:
                        prod_war = ProductAtWarehouse.objects.get(product=old.product, warehouse=old.purchase.warehouse, price=old.acceptance_price)
                        prod_war.amount -= old.return_amount
                        prod_war.save()
                        if not prod_war.amount:
                            prod_war.delete()
                    except ProductAtWarehouse.DoesNotExist:
                        print 'DoesNotExist'
                failure = u'На складе: ' + product.purchase.warehouse.name + u' невозможно сделать возврат по товару: ' + product.product.name + u' , так как его не осталось '
                return render_to_response('warehouse/return.html',{'form_return'        :   form_return,
                                                                   'acceptance'         :   acceptance,
                                                                   'products'           :   product_list,
                                                                   'form_products'      :   form_products,
                                                                   'failure'            :   failure
                },RequestContext(request))
        return_m.save()
        form_products.save()

        for product in acceptance.purchase.productofpurchase_set.all():
            try:
                prod_war = ProductAtWarehouse.objects.get(product=product.product, warehouse=product.purchase.warehouse, price=product.acceptance_price)
                prod_war.amount -= product.return_amount
                prod_war.save()
                if not prod_war.amount:
                    prod_war.delete()
            except ProductAtWarehouse.DoesNotExist:
                print 'DoesNotExist'
        return HttpResponseRedirect('/returns/page/1')
    return render_to_response('warehouse/return.html',{'form_return'        :   form_return,
                                                       'acceptance'         :   acceptance,
                                                       'products'           :   product_list,
                                                       'form_products'      :   form_products,
                                                       'failure'            :   failure
    },RequestContext(request))

@login_required()
def returns(request, page_pk):
    page_pk = int(page_pk)
    per_page = 10
    returns = ReturnModel.objects.all().order_by('date','pk')
    all = returns.count()
    pages = int(ceil(all/float(per_page)))
    if page_pk>pages and page_pk!=1:
        raise  Http404()
    page_list = []
    for i in range(pages):
        page_list.append(i+1)
    prev = 1
    if page_pk!=1:
        prev = page_pk -1
    if page_pk==pages:
        next = page_pk
    else:
        next = page_pk + 1
    range_date = request.POST.get('report_range', '')
    if range_date!='':
        start = range_date[:10]
        end = range_date[14:]
        try:
            returns = returns.filter(date__gte=start, date__lte=end)
        except :
            print 'bad date request'
    returns = returns[per_page*page_pk-per_page:per_page*page_pk]
    return render_to_response('warehouse/returns.html',{'returns'     :   returns,
                                                            'range'       :   range_date,
                                                            'pages'       :   page_list,
                                                            'current'     :   page_pk,
                                                            'prev'        :   prev,
                                                            'next'        :   next
    }, RequestContext(request))

