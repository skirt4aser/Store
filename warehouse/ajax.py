# -*- coding: utf-8 -*-
import datetime
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404
from database.models import Purchase, Product

__author__ = 'Ars'

def purchase_save(request):
    if request.is_ajax():
        purchase = get_object_or_404(Purchase, pk=request.POST.get('id_purchase', ''))
        text = 'ok'
        try:
            purchase.supplier_id = request.POST.get('id_supplier', '')
            purchase.purchaser_id = request.POST.get('id_purchaser', '')
            purchase.warehouse_id = request.POST.get('id_warehouse', '')
            purchase.date_purchase = request.POST.get('date_purchase', '')
            purchase.comment = request.POST.get('comment', '')
            issued = request.POST.get('issued')
            if issued=='':
                issued = None
            purchase.issued = issued
            purchase.modified_date = datetime.date.today()
            purchase.modified_author = request.user
            purchase.save()
        except :
            text = u'Неправильно заполнены поля'
        return HttpResponse(text,mimetype="text/html")
    else:
        return HttpResponseForbidden()

def get_product_price(request):
    if request.is_ajax():
        product = get_object_or_404(Product, pk=request.POST.get('id_product', ''))
        return HttpResponse(product.price,mimetype="text/html")
    else:
        return HttpResponseForbidden()