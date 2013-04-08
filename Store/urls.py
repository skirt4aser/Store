from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from warehouse.ajax import purchase_save, get_product_price
from warehouse.views import purchases, purchase, purchase_product_delete, purchase_product, purchase_delete, acceptance, acceptances, return_view

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    (r'^purchases/page/(?P<page_pk>\d+)/$', purchases),
    (r'^purchase/$', purchase, {'id_purchase':0}),
    (r'^purchase/(?P<id_purchase>\d+)/$', purchase),
    (r'^purchase/(?P<id_purchase>\d+)/product/(?P<id_product>\d+)/$', purchase_product),
    (r'^purchase/product/(?P<id_product>\d+)/delete/$', purchase_product_delete),
    (r'^purchase/(?P<id_purchase>\d+)/delete/$', purchase_delete),

    (r'^ajax/purchase/save/$', purchase_save),
    (r'^ajax/purchase/get_product_price/$', get_product_price),

    (r'^purchase/(?P<id_purchase>\d+)/acceptance/$', acceptance),
    (r'^acceptances/page/(?P<page_pk>\d+)/$', acceptances),

    (r'^acceptance/(?P<id_acceptance>\d+)/return/$', return_view),
)
