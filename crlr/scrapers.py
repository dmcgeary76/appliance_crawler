from selenium import webdriver
from bs4 import BeautifulSoup as bs, NavigableString, Comment
from django.shortcuts import get_object_or_404
from .models import Basic_Model, Appliance_Model
from urllib.parse import urljoin
import requests
import re


def add_models():
    starturl = 'https://www.bestbuy.com/site/washers-dryers/dryers/abcat0910004.c?id=abcat0910004'
    basic_model = Basic_Model(appliance_type='Dryer', store_name='Best Buy', start_url=starturl)
    basic_model.save()

    starturl = 'https://www.bestbuy.com/site/microwaves/all-microwaves/pcmcat748301803023.c?id=pcmcat748301803023'
    basic_model = Basic_Model(appliance_type='Microwave', store_name='Best Buy', start_url=starturl)
    basic_model.save()

    starturl = 'https://www.bestbuy.com/site/heating-cooling-air-quality/air-conditioners/abcat0907001.c?id=abcat0907001'
    basic_model = Basic_Model(appliance_type='Air Conditioner', store_name='Best Buy', start_url=starturl)
    basic_model.save()

    starturl = 'https://www.bestbuy.com/site/heating-cooling-air-quality/dehumidifiers/abcat0908002.c?id=abcat0908002'
    basic_model = Basic_Model(appliance_type='Dehumidifier', store_name='Best Buy', start_url=starturl)
    basic_model.save()

    starturl = 'https://www.bestbuy.com/site/vacuums-floor-care/all-vacuums-and-floor-care/pcmcat338600050020.c?id=pcmcat338600050020'
    basic_model = Basic_Model(appliance_type='Vacuum', store_name='Best Buy', start_url=starturl)
    basic_model.save()


def _extract_prices(item):
    price_texts = [
        el.get_text(" ", strip=True)
        for el in item.select(
            "[data-testid*='price'], "
            ".priceView-hero-price, "
            ".priceView-customer-price, "
            ".pricing-price__regular-price, "
            ".pricing-price__sale-price"
        )
    ]
    if not price_texts:
        price_texts = [item.get_text(" ", strip=True)]
    price_numbers = re.findall(r"\d+\.\d{2}", " ".join(price_texts))
    return sorted({float(value) for value in price_numbers})


def _extract_image_url(item, sku):
    for img in item.select("img"):
        candidate = img.get("data-src") or img.get("src") or ""
        if not candidate:
            continue
        if sku and sku in candidate:
            return urljoin("https://", candidate)
        if "pisces.bbystatic" in candidate:
            return urljoin("https://", candidate)
    match = re.search(r"pisces\.bbystatic\S+", str(item))
    if match:
        return "https://" + match.group()
    return ""


def update_appliance_list(soup, basic_model):
    # isolate the item records
    items = soup.find_all('div', {'class': 'list-item'})

    # strip out the info from each item on the page and store it
    for item in items:
        try:
            has_sale_price = bool(
                item.select_one("[class*='onSale'], [data-testid*='sale']")
            ) or "onSale" in str(item)
            sku_title = item.select_one("div.sku-title") or item.select_one(
                "[data-testid='product-title']"
            )
            title_text = sku_title.get_text(" ", strip=True) if sku_title else ""
            title_parts = [part.strip() for part in title_text.split(" - ") if part.strip()]
            manufacturer = title_parts[0] if len(title_parts) > 0 else ""
            short_description = title_parts[1] if len(title_parts) > 1 else title_text
            color = title_parts[2] if len(title_parts) > 2 else ""

            sku_values = [span.get_text(strip=True) for span in item.select("span.sku-value")]
            model_number = sku_values[0] if len(sku_values) > 0 else ""
            sku = sku_values[1] if len(sku_values) > 1 else item.get("data-sku-id", "")
            if not sku:
                continue

            price_list = _extract_prices(item)
            if not price_list:
                continue
            fprice = price_list[-1]
            if has_sale_price and len(price_list) >= 2:
                sprice = price_list[-2]
                obprice = price_list[-3] if len(price_list) >= 3 else 0.00
            else:
                sprice = price_list[-1]
                obprice = price_list[-2] if len(price_list) >= 2 else 0.00

            imgurl = _extract_image_url(item, sku)

            deleted, _ = Appliance_Model.objects.filter(sku=str(sku)).delete()
            if deleted:
                print(str(sku) + ' exists and will be deleted.')

            app_model = Appliance_Model(
                basic_model=basic_model,
                short_description=short_description,
                manufacturer=manufacturer,
                color=color,
                model_number=model_number,
                sku=str(sku),
                full_price=fprice,
                sale_price=sprice,
                open_box_price=obprice,
                img_url=imgurl.split(";")[0]
            )
            print('Record inserted for ' + app_model.manufacturer + ' ' + app_model.sku)
            app_model.save()
        except Exception:
            pass


def main(app_type, store_name, count = 1):
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
        while not done:
            # Set options for the web-driver - including headless
            options = webdriver.ChromeOptions()
            options.add_argument('headless') #collect web info without an actual window
            options.add_argument('--no-sandbox') # take off the training wheels
            options.add_argument('window-size=1200x600') # set the window size

            # assign webdriver to a driver instance
            driver = None
            try:
                driver = webdriver.Chrome(options=options)

            if count == 1:
                start_url = basic_model.start_url
            else:
                start_url = basic_model.start_url.split('?')[0] + '?cp=' + str(count) + '&' + basic_model.start_url.split('?')[1]
                try:
                    # get the page again to see if the content has changed
                    driver.get(start_url)
                    soup = bs(driver.page_source, 'html.parser')
                    update_appliance_list(soup, basic_model)
                    print('THIS IS PAGE ' + str(count))
                    count += 1
                except:
                    done = True
                    print(count)
                    print('Done')
            finally:
                if driver:
                    driver.quit()


def update_all():
    app_type = ['Refrigerator', 'Washing Machine', 'Dishwasher', 'Dryer', 'Microwave', 'Air Conditioner', 'Dehumidifier', 'Vacuum']
    for appl in app_type:
        try:
            main(appl, 'Best Buy')
        except:
            pass
