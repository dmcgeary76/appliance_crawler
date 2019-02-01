import csv
from selenium import webdriver
from bs4 import BeautifulSoup as bs

# Set a target url so that we have some way to move through pages
target_url = 'http://e-cfisd.hcde-texas.org/report/outline/index.php?id='

# Set options for the web-driver - including headless
options = webdriver.ChromeOptions()
options.add_argument('headless') #collect web info without an actual window
options.add_argument('--no-sandbox') # take off the training wheels
options.add_argument('window-size=1200x600') # set the window size

# assign webdriver to a driver instance
driver = webdriver.Chrome(chrome_options=options)

# get the login page of interest
driver.get('http://e-cfisd.hcde-texas.org')

# wait for up to 10 seconds to get the page data
driver.implicitly_wait(10)

# find the login fields on the page
username = driver.find_element_by_css_selector('input[id=login_username]')
password = driver.find_element_by_css_selector('input[id=login_password]')

# find the login button
login_btn = driver.find_element_by_css_selector('input[value="Log in"]')

# take a screenshot just to test that everything is working as it should.
driver.get_screenshot_as_file('moodle1.png')

# If all looks good, click to login_btn
login_btn.click()

done = False
coursenum = 4893

records = [[]]

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

with open('test.csv', "w") as f:
    writer = csv.writer(f)
    first_row = 'Title, Status, '
    done = False
    i = 0
    while not done:
        first_row = first_row + 'Activity_Title_' + str(i+1) + ', Activity_Users_' + str(i+1)
        i += 1
        if i == 39:
            done = True
    writer.writerow(first_row)
    for record in records:
        row = []
        for item in record:
            if isinstance(item, str):
                row.append(item.replace('"', ''))
            else:
                row.append(', '.join(item))
        writer.writerow(row)
