from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from database.models import Supplier
from catalog.forms import SupplierForm
#from django.utils import simplejson


def supplier(request):
    print('SUPPLIER GET')
    # returns populated form, if id is present,
    # blank form otherwise
    try:
        id = request.POST['id']
    except:
        print ('ERROR: id is not found...')
    else:
        print ('got id', id)
        obj = get_object_or_404(Supplier, pk=id)
        form = SupplierForm(instance=obj)
        return render_to_response('catalog/modal_supplier.html', {'form': form}, context_instance=RequestContext(request))

    form = SupplierForm()
    return render_to_response('catalog/modal_supplier.html', {'form': form}, context_instance=RequestContext(request))


def supplier_save(request):
    print('SUPPLIER SAVE')
    print(request)
    return HttpResponse('{success:true}')


def supplier_delete(request):
    print('SUPPLIER DELETE')


# def ajax_test(request):
#     context = {}
#     try:
#         data = request.POST['text'].strip()
#     except:
#         context['text'] = 'error'
#         print (context['text'])
#     else:
#         context['text'] = data[::-1]
#         print (context['text'])
#     return HttpResponse(context['text'])
