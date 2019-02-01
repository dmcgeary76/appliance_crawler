from selenium import webdriver
from bs4 import BeautifulSoup as bs, NavigableString, Comment
from django.shortcuts import get_object_or_404
from .models import Basic_Model, Appliance_Model
import re


def get_appliance_list():
    # Set a start_url value to test
    start_url = 'https://www.bestbuy.com/site/refrigerators/all-refrigerators/pcmcat367400050001.c?id=pcmcat367400050001'
    # Need a basic model to use as a ForeignKey
    #basic_model = get_object_or_404(Basic_Model, appliance_type='Refrigerator')

    # Set options for the web-driver - including headless
    options = webdriver.ChromeOptions()
    options.add_argument('headless') #collect web info without an actual window
    options.add_argument('--no-sandbox') # take off the training wheels
    options.add_argument('window-size=1200x600') # set the window size

    # assign webdriver to a driver instance
    driver = webdriver.Chrome(chrome_options=options)

    # wait for up to 10 seconds to get the page data
    driver.implicitly_wait(10)

    # get the login page again to see if the content has changed
    driver.get(start_url)
    soup = bs(driver.page_source, 'html.parser')

    # isolate the item records
    items = soup.find_all('div', {'class':'list-item'})

    # strip out the info from each item on the page and store it
    for item in items:
        has_sale_price = False
        if ('onSale' in str(item)):
            has_sale_price = True
        short_descs = item.find_all('div', {'class':'sku-title'})
        model_sku = item.find_all('span', {'class': 'sku-value'})
        pattern = re.compile(r'\d+\.\d\d')
        prices = pattern.finditer(str(item))
        price_list = []
        for price in prices:
            if float(price.group()) not in price_list:
                price_list.append(float(price.group()))
                price_list.sort()
                print(price_list)
        # Set values for the entries
        fprice = price_list[-1]
        if has_sale_price:
            sprice  = price_list[-2]
            obprice = price_list[-3]
        else:
            sprice  = price_list[-1]
            obprice = price_list[-2]
        app_model = Appliance_Model(
            short_description   = short_descs[0].text.strip().split(' - ')[1],
            manufacturer        = short_descs[0].text.strip().split(' - ')[0],
            color               = short_descs[0].text.strip().split(' - ')[2],
            model_number        = model_sku[0].text.strip(),
            sku                 = model_sku[1].text.strip(),
            full_price          = fprice,
            sale_price          = sprice,
            open_box_price      = obprice
        )
        print(app_model.manufacturer)
        print(app_model.short_description)
        print(app_model.color)
        print(app_model.model_number)
        print(app_model.sku)
        print('Full Price: ' + str(app_model.full_price))
        print('Sale Price: ' + str(app_model.sale_price))
        print('Open Box Price: ' + str(app_model.open_box_price))
        print('----------------------------------------')


'''
while not done:
    # Increment the counter
    coursenum += 1

    # Initialize a temp record as a holder
    temp_record = [[]]

    # get the teacher name to add to the text header for the report
    driver.get('http://e-cfisd.hcde-texas.org/enrol/users.php?id=' + str(coursenum))

    # get the login page again to see if the content has changed
    driver.get('http://e-cfisd.hcde-texas.org/report/outline/index.php?id=' + str(coursenum))
    soup = bs(driver.page_source, 'html.parser')

    # Add course title to record
    temp_record.append(soup.find('h2').text.strip())
    temp_record.append('')

    # Collect all of the table rows from the report page_source
    rows = soup.find_all('tr')

    for row in rows:
        try:
            col = row.find('td', {'class':'numviews'})
            if col.text.strip() != '-':
                small_set = []
                small_set.append(row.find('td', {'class':'activity'}).text.strip())
                small_set.append(row.find('td', {'class':'numviews'}).text.strip().split(' by ')[1])
                print(small_set)
                temp_record.append(small_set)
        except:
            pass

    temp_record.pop(0)
    if len(temp_record) == 2:
        temp_record.pop()
        temp_record.append('There is no record of student activity in this course.')
    records.append(temp_record)

    # Terminate the while statement after the last course record
    if coursenum == 4894:
        done = True

records.pop(0)
'''
