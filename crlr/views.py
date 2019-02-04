from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from .models import Appliance_Model, OpenBox_Model
from .forms import Appliance_Filter_Form
import csv
import io


# Create your views here.
def list_view(request):
    appliances = Appliance_Model.objects.all()
    filter_form = Appliance_Filter_Form(request.GET or None)
    if request.method == 'GET': # If the form is submitted
        manufacturer_sort_term = request.GET.get('manufacturer_sort', None)
        price_sort_term = request.GET.get('price_sort', None)
        # Reset the form
        if manufacturer_sort_term and price_sort_term:
            appliances = Appliance_Model.objects.all().filter(manufacturer = manufacturer_sort_term).order_by(price_sort_term)
            request.session['manufacturer_sort'] = manufacturer_sort_term
            request.session['price_sort'] = price_sort_term
        elif manufacturer_sort_term:
            appliances = Appliance_Model.objects.all().filter(manufacturer = manufacturer_sort_term)
            request.session['manufacturer_sort'] = manufacturer_sort_term
            request.session['price_sort'] = None
        elif price_sort_term:
            appliances = Appliance_Model.objects.all().order_by(price_sort_term)
            request.session['manufacturer_sort'] = None
            request.session['price_sort'] = price_sort_term
        else:
            request.session['manufacturer_sort'] = None
            request.session['price_sort'] = None
    context = {
        'appliances': appliances,
        'filter_form': filter_form
    }
    return render(request, 'list.html', context)


def csv_view(request):
    appliances = Appliance_Model.objects.all()
    buffer = io.StringIO()
    wr = csv.writer(buffer, quoting=csv.QUOTE_ALL)
    row = 'Manufacturer, Short Description, Color, Model Number, SKU, Full Price, Sale Price, Open Box Price, Image URL'
    wr.writerow(row)
    for appliance in appliances:
        row = []
        row.append(appliance.manufacturer)
        row.append(appliance.short_description)
        row.append(appliance.color)
        row.append(appliance.model_number)
        row.append(appliance.sku)
        row.append(appliance.full_price)
        row.append(appliance.sale_price)
        row.append(appliance.open_box_price)
        row.append(appliance.img_url)
        wr.writerow(row)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=appliance_list.csv'
    return response


def search_view(request):
    form = Search_Form(request.POST or None)
    if form.is_valid():
        form.save()
        context = {
            'form': form
        }
    return render(request, 'list.html', context)
