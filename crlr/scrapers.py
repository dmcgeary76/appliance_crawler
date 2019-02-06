from selenium import webdriver
from bs4 import BeautifulSoup as bs, NavigableString, Comment
from django.shortcuts import get_object_or_404
from .models import Basic_Model, Appliance_Model
import requests
import re


def add_model():
    starturl = 'https://www.bestbuy.com/site/washers-dryers/washers-washing-machines/abcat0910001.c?id=abcat0910001'
    basic_model = Basic_Model(appliance_type='Washing Machine', store_name='Best Buy', start_url=starturl)
    basic_model.save()

def update_appliance_list(soup, basic_model):
    # isolate the item records
    items = soup.find_all('div', {'class':'list-item'})

    # strip out the info from each item on the page and store it
    for item in items:
        try:
            has_sale_price = False
            if ('onSale' in str(item)):
                has_sale_price = True
            short_descs = item.find_all('div', {'class':'sku-title'})
            model_sku = item.find_all('span', {'class': 'sku-value'})
            img_pattern = re.compile(r'pisces.bbystatic\S+')
            temp_imgurl = img_pattern.finditer(str(item))
            for url in temp_imgurl:
                if model_sku[1].text.strip() in url.group():
                    imgurl = 'https://' + url.group()
            pattern = re.compile(r'\d+\.\d\d')
            prices = pattern.finditer(str(item))
            price_list = []
            for price in prices:
                if float(price.group()) not in price_list:
                    price_list.append(float(price.group()))
                    price_list.sort()
            # Set values for the entries
            fprice = price_list[-1]
            if has_sale_price:
                sprice  = price_list[-2]
                obprice = price_list[-3]
            else:
                try:
                    sprice  = price_list[-1]
                    obprice = price_list[-2]
                except:
                    sprice = price_list[-1]
                    obprice = 0.00
            try:
                app_model = get_object_or_404(Appliance_Model, sku = str(model_sku[1].text.strip()))
                print(app_model.sku + ' exists and will be deleted.')
                app_model.delete()
            except:
                pass
            finally:
                app_model = Appliance_Model(
                    basic_model         = basic_model,
                    short_description   = short_descs[0].text.strip().split(' - ')[1],
                    manufacturer        = short_descs[0].text.strip().split(' - ')[0],
                    color               = short_descs[0].text.strip().split(' - ')[2],
                    model_number        = model_sku[0].text.strip(),
                    sku                 = str(model_sku[1].text.strip()),
                    full_price          = fprice,
                    sale_price          = sprice,
                    open_box_price      = obprice,
                    img_url             = imgurl.split(';')[0]
                )
                print('Record inserted for ' + app_model.manufacturer + ' ' + app_model.sku)
                app_model.save()
        except:
            pass


def main(app_type, store_name):
    try:
        basic_model = get_object_or_404(Basic_Model, appliance_type=app_type, store_name=store_name)
    except:
        if app_type == 'Refrigerator':
            starturl = 'https://www.bestbuy.com/site/refrigerators/all-refrigerators/pcmcat367400050001.c?cp=31&id=pcmcat367400050001'
        elif apptype == 'Dishwasher':
            starturl = 'https://www.bestbuy.com/site/dishwashers/built-in-dishwashers/abcat0905001.c?id=abcat0905001'
        elif apptype == 'Washing Machine':
            starturl = 'https://www.bestbuy.com/site/washers-dryers/washers-washing-machines/abcat0910001.c?id=abcat0910001'
        basic_model = Basic_Model(appliance_type=appliance_type, store_name='Best Buy', start_url=starturl)
        basic_model.save()
    finally:
        done = False
        count = 1
        while not done:
            # Set options for the web-driver - including headless
            options = webdriver.ChromeOptions()
            options.add_argument('headless') #collect web info without an actual window
            options.add_argument('--no-sandbox') # take off the training wheels
            options.add_argument('window-size=1200x600') # set the window size

            # assign webdriver to a driver instance
            driver = webdriver.Chrome(chrome_options=options)

            if count == 1:
                start_url = basic_model.start_url
            else:
                start_url = basic_model.start_url.split('?')[0] + '?cp=' + str(count) + '&' + basic_model.start_url.split('?')[1]
            try:
                # get the page again to see if the content has changed
                driver.get(start_url)
                soup = bs(driver.page_source, 'html.parser')
                update_appliance_list(soup, basic_model)
                count += 1
            except:
                done = True
                print(count)
                print('Done')


'''
https://www.bestbuy.com/site/refrigerators/all-refrigerators/pcmcat367400050001.c?id=pcmcat367400050001
https://www.bestbuy.com/site/refrigerators/all-refrigerators/pcmcat367400050001.c?cp=31&id=pcmcat367400050001
'''
