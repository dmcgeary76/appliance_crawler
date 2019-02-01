from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .scrapers import get_appliance_list
from .models import Appliance_Model, OpenBox_Model


# Create your views here.
@login_required
def refrigerator_view(request):
    basic_model = Basic_Model.objects.get(appliance_type='Refrigerator')
    get_appliance_list(basic_model.start_url)






https://www.bestbuy.com/site/refrigerators/all-refrigerators/pcmcat367400050001.c?id=pcmcat367400050001
https://www.bestbuy.com/site/refrigerators/all-refrigerators/pcmcat367400050001.c?cp=3&id=pcmcat367400050001
