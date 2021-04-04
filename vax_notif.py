import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
import requests


def loadHeadlessBrowser():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    return webdriver.Firefox(options=options)


driver = loadHeadlessBrowser()
print("Loaded Browser")
url = "https://covid.northernlighthealth.org/Vaccine/Vaccination-Request-Form-Home"

while True:
    print("Running...")
    # load page
    driver.get(url)

    # select location
    location = Select(driver.find_element_by_name("p$lt$ctl00$pageplaceholder$p$lt$ctl00$EmployeeRequestForm_FirstAppointment$ddLocation"))
    location.select_by_value('18')
    time.sleep(5)

    # parse
    html = driver.page_source
    page = BeautifulSoup(html, 'html.parser')

    # get dates
    dateOptions = driver.find_element_by_id("p_lt_ctl00_pageplaceholder_p_lt_ctl00_EmployeeRequestForm_FirstAppointment_ddAppointmentDate")
    dates = [x for x in dateOptions.find_elements_by_tag_name("option")]

    # send notification
    if len(dates) > 1:
        def getDates(x):
            string = "\n"
            for element in dates:
                if element.get_attribute("innerHTML") != "Choose...":
                    string = string + str(element.get_attribute("innerHTML")) + "\n"
            return string

        r = requests.post("https://api.pushover.net/1/messages.json",
                          data={'token': 'API_TOKEN',   # enter your pushover api token
                                'user': 'USER ID',   # enter your user token
                                'message': 'Sign up now!\n' + url + getDates(dates)})
    else:
        print("No dates available.")

    time.sleep(120)
