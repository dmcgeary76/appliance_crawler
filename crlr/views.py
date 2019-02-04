from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Appliance_Model, OpenBox_Model
from .forms import Appliance_Filter_Form


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
        elif manufacturer_sort_term:
            appliances = Appliance_Model.objects.all().filter(manufacturer = manufacturer_sort_term)
        elif price_sort_term:
            appliances = Appliance_Model.objects.all().order_by(price_sort_term)
    context = {
        'appliances': appliances,
        'filter_form': filter_form
    }
    return render(request, 'list.html', context)


def search_view(request):
    form = Search_Form(request.POST or None)
    if form.is_valid():
        form.save()
        context = {
            'form': form
        }
    return render(request, 'list.html', context)
