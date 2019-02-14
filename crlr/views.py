from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from .models import Appliance_Model, OpenBox_Model
from .forms import Dishwasher_Filter_Form, Refrigerator_Filter_Form, Washing_Machine_Filter_Form, Dryer_Filter_Form, Microwave_Filter_Form
from .forms import Air_Conditioner_Filter_Form, Dehumidifier_Filter_Form, Vacuum_Filter_Form
import csv
import io


# Create your views here.
def list_view(request, basic_model_id = 0):
    appliances = Appliance_Model.objects.all().filter(basic_model_id = basic_model_id)
    if basic_model_id == 0:
        basic_model_id = request.session['basic_model_id']
    else:
        request.session['basic_model_id'] = basic_model_id
    manufacturer_tag = 'All'
    if basic_model_id == 1:
        filter_form = Refrigerator_Filter_Form(request.GET or None)
    elif basic_model_id == 2:
        filter_form = Dishwasher_Filter_Form(request.GET or None)
    elif basic_model_id == 3:
        filter_form = Washing_Machine_Filter_Form(request.GET or None)
    elif basic_model_id == 4:
        filter_form = Dryer_Filter_Form(request.GET or None)
    elif basic_model_id == 5:
        filter_form = Microwave_Filter_Form(request.GET or None)
    elif basic_model_id == 6:
        filter_form = Air_Conditioner_Filter_Form(request.GET or None)
    elif basic_model_id == 7:
        filter_form = Dehumidifier_Filter_Form(request.GET or None)
    elif basic_model_id == 8:
        filter_form = Vacuum_Filter_Form(request.GET or None)
    if request.method == 'GET': # If the form is submitted
        manufacturer_sort_term = request.GET.get('manufacturer_sort', None)
        price_sort_term = request.GET.get('price_sort', None)
        # Reset the form
        if manufacturer_sort_term and price_sort_term:
            appliances = Appliance_Model.objects.all().filter(basic_model_id = basic_model_id, manufacturer = manufacturer_sort_term).order_by(price_sort_term)
            request.session['manufacturer_sort'] = manufacturer_sort_term
            manufacturer_tag = manufacturer_sort_term
            request.session['price_sort'] = price_sort_term
        elif manufacturer_sort_term:
            appliances = Appliance_Model.objects.all().filter(basic_model_id = basic_model_id, manufacturer = manufacturer_sort_term)
            request.session['manufacturer_sort'] = manufacturer_sort_term
            manufacturer_tag = manufacturer_sort_term
            request.session['price_sort'] = None
        elif price_sort_term:
            appliances = Appliance_Model.objects.all().filter(basic_model_id = basic_model_id).order_by(price_sort_term)
            request.session['manufacturer_sort'] = None
            request.session['price_sort'] = price_sort_term
        else:
            request.session['manufacturer_sort'] = None
            request.session['price_sort'] = None
    context = {
        'appliances': appliances,
        'filter_form': filter_form,
        'manufacturer_tag': manufacturer_tag,
        'basic_model_id': basic_model_id,
    }
    return render(request, 'list.html', context)


def csv_view(request):
    if request.session['manufacturer_sort'] and request.session['price_sort']:
        appliances = Appliance_Model.objects.all().filter(basic_model_id = request.session['basic_model_id'],manufacturer = request.session['manufacturer_sort']).order_by(request.session['price_sort'])
    elif request.session['manufacturer_sort']:
        appliances = Appliance_Model.objects.all().filter(basic_model_id = request.session['basic_model_id'],manufacturer = request.session['manufacturer_sort'])
    elif request.session['price_sort']:
        appliances = Appliance_Model.objects.all().filter(basic_model_id = request.session['basic_model_id']).order_by(request.session['price_sort'])
    else:
        appliances = Appliance_Model.objects.all().filter(basic_model_id = request.session['basic_model_id'])
    buffer = io.StringIO()
    wr = csv.writer(buffer, quoting=csv.QUOTE_ALL)
    row = ['Manufacturer', 'Short Description', 'Color', 'Model Number', 'SKU', 'Full Price', 'Sale Price', 'Open Box Price', 'Image URL']
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


def home_view(request):
    return render(request, 'home.html', {})
