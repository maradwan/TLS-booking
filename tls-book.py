import time
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from sendEmail import send_to_me
from bs4 import BeautifulSoup

def login(driver): 

    if 'myapp' in driver.current_url:
        print('refresh')
        driver.refresh() 
        return True
    else:
        driver.get('https://de-legalization.tlscontact.com/eg/CAI/login.php')
        email = driver.find_element_by_id("email")
        email.clear()
        # TODO add here !! 
        email.send_keys('your registerd email')

        passwd = driver.find_element_by_id('pwd')
        passwd.clear()
        # TODO add here!! 
        passwd.send_keys('password')

        driver.find_element_by_class_name("submit").click()

        delay = 5 # seconds
        time.sleep(delay)

        if 'myapp' in driver.current_url:
            print('Login Successful')
            return True
        
        else:
            print('Login Unuccessful !!')
            return False



def is_an_appointment_free(driver):
    table = driver.find_element_by_id('timeTable')   
    tableContent = BeautifulSoup(table.get_attribute('innerHTML'), features="html.parser")

    days = tableContent.find_all("span", {"class": "appt-table-d"})
    other_day = False
    str_days = str(days)

    # TODO edit as the days u see now!! 
    if '16' not in str_days or '17' not in str_days:
        print('day')
        other_day = True   

    # TODO edit as the slots u see now!! 
    appointments = tableContent.find_all("a")
    full = True
    for appointment in appointments: 
        str_appointment = str(appointment)
        if 'full' not in str_appointment:
            full = False  
    
    # TODO edit!! 
    if not full or other_day or len(appointments) != 14 or len(days) != 2:
        print('Appointment found')
        return True
    else: 
        print('No found')
        return False



def check(driver):
    try:
        if login(driver) and is_an_appointment_free(driver):
            title = 'TLS Appointment is free'
            message = 'Luke, Iam your father ... U have to go there now => https://de-legalization.tlscontact.com/eg/CAI/login.php'
            send_to_me(message, title)

    except Exception as e: 
        title = 'Somnthing went wrong'
        message = str(e)
        print(message)
        # send_to_me(message, title)



firefoxOptions = Options()
firefoxOptions.add_argument("-headless")
driver = webdriver.Firefox(executable_path="./drivers/geckodriver", options=firefoxOptions)

while 1:
    print(datetime.datetime.now())
    check(driver)
    print(' -------------------------------------------------------- ')
    time.sleep(5 * 60)

