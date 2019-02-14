from django import forms
from .models import Appliance_Filter_Model, Appliance_Model

price_list = [
    ('','Filter By Price',),
    ('full_price', 'Full Price',),
    ('sale_price', 'Sale_Price',),
    ('open_box_price', 'Open Box Price',)
]

class Refrigerator_Filter_Form(forms.ModelForm):
    manufacturer_sort   = forms.ModelChoiceField(
                                    queryset=Appliance_Model.objects.all().filter(basic_model_id = 1).values_list('manufacturer', flat=True).distinct().order_by('manufacturer'),
                                    required=False)
    price_sort          = forms.ChoiceField(
                                    choices = price_list,
                                    required=False)
    class Meta:
        model = Appliance_Filter_Model
        fields = [
            'manufacturer_sort',
            'price_sort'
        ]


class Dishwasher_Filter_Form(forms.ModelForm):
    manufacturer_sort   = forms.ModelChoiceField(
                                    queryset=Appliance_Model.objects.all().filter(basic_model_id = 2).values_list('manufacturer', flat=True).distinct().order_by('manufacturer'),
                                    required=False)
    price_sort          = forms.ChoiceField(
                                    choices = price_list,
                                    required=False)
    class Meta:
        model = Appliance_Filter_Model
        fields = [
            'manufacturer_sort',
            'price_sort'
        ]


class Washing_Machine_Filter_Form(forms.ModelForm):
    manufacturer_sort   = forms.ModelChoiceField(
                                    queryset=Appliance_Model.objects.all().filter(basic_model_id = 3).values_list('manufacturer', flat=True).distinct().order_by('manufacturer'),
                                    required=False)
    price_sort          = forms.ChoiceField(
                                    choices = price_list,
                                    required=False)
    class Meta:
        model = Appliance_Filter_Model
        fields = [
            'manufacturer_sort',
            'price_sort'
        ]


class Dryer_Filter_Form(forms.ModelForm):
    manufacturer_sort   = forms.ModelChoiceField(
                                    queryset=Appliance_Model.objects.all().filter(basic_model_id = 4).values_list('manufacturer', flat=True).distinct().order_by('manufacturer'),
                                    required=False)
    price_sort          = forms.ChoiceField(
                                    choices = price_list,
                                    required=False)
    class Meta:
        model = Appliance_Filter_Model
        fields = [
            'manufacturer_sort',
            'price_sort'
        ]


class Microwave_Filter_Form(forms.ModelForm):
    manufacturer_sort   = forms.ModelChoiceField(
                                    queryset=Appliance_Model.objects.all().filter(basic_model_id = 5).values_list('manufacturer', flat=True).distinct().order_by('manufacturer'),
                                    required=False)
    price_sort          = forms.ChoiceField(
                                    choices = price_list,
                                    required=False)
    class Meta:
        model = Appliance_Filter_Model
        fields = [
            'manufacturer_sort',
            'price_sort'
        ]


class Air_Conditioner_Filter_Form(forms.ModelForm):
    manufacturer_sort   = forms.ModelChoiceField(
                                    queryset=Appliance_Model.objects.all().filter(basic_model_id = 6).values_list('manufacturer', flat=True).distinct().order_by('manufacturer'),
                                    required=False)
    price_sort          = forms.ChoiceField(
                                    choices = price_list,
                                    required=False)
    class Meta:
        model = Appliance_Filter_Model
        fields = [
            'manufacturer_sort',
            'price_sort'
        ]


class Dehumidifier_Filter_Form(forms.ModelForm):
    manufacturer_sort   = forms.ModelChoiceField(
                                    queryset=Appliance_Model.objects.all().filter(basic_model_id = 7).values_list('manufacturer', flat=True).distinct().order_by('manufacturer'),
                                    required=False)
    price_sort          = forms.ChoiceField(
                                    choices = price_list,
                                    required=False)
    class Meta:
        model = Appliance_Filter_Model
        fields = [
            'manufacturer_sort',
            'price_sort'
        ]


class Vacuum_Filter_Form(forms.ModelForm):
    manufacturer_sort   = forms.ModelChoiceField(
                                    queryset=Appliance_Model.objects.all().filter(basic_model_id = 8).values_list('manufacturer', flat=True).distinct().order_by('manufacturer'),
                                    required=False)
    price_sort          = forms.ChoiceField(
                                    choices = price_list,
                                    required=False)
    class Meta:
        model = Appliance_Filter_Model
        fields = [
            'manufacturer_sort',
            'price_sort'
        ]
