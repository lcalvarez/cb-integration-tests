#!/usr/bin/python

# ---------------------------------------------------------------------------
# Author: Luis Alvarez
# File Description

# Imports -------------------------------------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import random
import string
import time
import ipdb

# <TODO> Docstring definition assumptions and arguments.

# Globals for waiting in between 
wait_time = 20
sleep_time = 5

# --------------------------Helper Functions---------------------------------
def id_generator(size=6, chars=string.ascii_letters + string.digits):
    """ 
    Returns a random combination of 
    characters for use in generating
    users     
    """
    return ''.join(random.choice(chars) for _ in range(size))
    
def create_info(ind=True):
    """
    Create necessary sender
    and recipient info
    
    Arguments:
    ind -- bool for individual info or business info
    Returns:

    sender_info -- dict of sender information
    recipient_info -- dict of recipient information        
    """
    
    sender_info = {'Firstname':'test-first'+id_generator(),
                   'Lastname':'test-last'+id_generator(),
                   'email':'testcb72+'+id_generator()+'@gmail.com',
                   'password':id_generator(),
                   'bank_username':'plaid_test',
                   'bank_password':'plaid_good'}
                 
    recipient_info = {'check_book_email':'testcb72+'+id_generator()+'@gmail.com',
                      'email':'testcb72@gmail.com',
                      'whole_name':'TestFirst TestLast',
                      'amount':str(random.randint(1,10)),
                      'memo':'Automated Test',
                      'email_password':'0o9i8u7y',
                      'online_passcode':'18715621'}
                      
    if ind:
        return sender_info, recipient_info
        
    else:
        sender_bus_info = {'incorporation_type':'Corporation',
                           'bus_name':'Test Bus Name'+id_generator(3),
                           'website':'Bus Website',
                           'bus_desc':'Bus Desc',
                           'avg_payment':'upto_1000',
                           'tax_id':'0011223344',
                           'phone':'5551234567',
                           'legal_first':'Legal-First',
                           'legal_last':'Legal-Last',
                           'street':'Street',
                           'city':'City',
                           'state':'State',
                           'zip':'ZIP',
                           'country':'Country'}
        
        return dict(sender_info.items()+sender_bus_info.items()), recipient_info

    
def wait_for_element(by,text,wait,error_msg):
    """
    Helper function to locate
    selenium objects    
    
    Arguments:
    
    by -- Selenium id locator
    text -- string to identify locator by     
    wait -- WebDriverWait instance
    error_msg -- string of message to print if error occurs
        
    Returns:
        
    element -- Object which selenium located
    """
    
    try:
        element = wait.until(EC.element_to_be_clickable((by,text))) 
    except:
        raise IOError(error_msg)
    return element
    
def choose_drop_down(element,text,driver):
    """
    Helper function to choose 
    a bank in a drop down menu    
    
    Arguments:
        
    element -- Selenium object 
    bank -- string of bank text
    driver -- Selenium webdriver    
    
    """
    select = Select(element)
    select.select_by_visible_text(text)
    driver.find_element(By.ID, "bank_user").send_keys('plaid_test')
    driver.find_element(By.ID, "bank_passwd").send_keys('plaid_good')
    driver.implicitly_wait(4*wait_time)
    time.sleep(sleep_time)
    
def verify_bank(wait,driver):
    """
    Helper function to
    verify bank account
    in the checkbook dashboard
    """
    
    driver.implicitly_wait(3*wait_time)
    time.sleep(2*sleep_time) 
    try:
        wait_for_element(By.ID,
                         'addUpdateButton',
                         wait,
                         "Can't find 'Verify My Bank' button").click()
    except:
        wait_for_element(By.ID,
                         'addUpdateButton',
                         wait,
                         "Can't find 'Verify My Bank' button").click()        

    driver.implicitly_wait(wait_time)
    time.sleep(sleep_time)
    
    choose_bank = wait_for_element(By.ID,
                                   'bank_name',
                                   wait,
                                   "No drop-down menu")        
                        
    choose_drop_down(choose_bank,'Wells Fargo',driver)

    driver.implicitly_wait(wait_time)
    
    wait_for_element(By.XPATH,
             '//button[contains(text(),"Submit")]',
             wait,
             "No 'Submit' Button").click()
             
    driver.implicitly_wait(3*wait_time)

    wait_for_element(By.XPATH,
                     '//button[contains(text(),"Complete")]',
                     wait,
                     "No 'Complete' Button").click()
    
    time.sleep(sleep_time)
    driver.implicitly_wait(4*wait_time)
# ---------------------------------------------------------------------------

# ----------------------------Process Functions------------------------------
def sign_up(info,driver):
    """     
    Sign up using info and browser 
    and get to the dashboard.

    Arguments:
    info -- dict of recipient info
    browser -- selenium webdriver instance
    """    
    
    # Move to home page
    base_url = "https://dev.checkbook.io"
    driver.get(base_url)
    
    # Wait for page to load
    time.sleep(sleep_time)
    wait = WebDriverWait(driver,wait_time)
    driver.implicitly_wait(2*wait_time)
    
    # Click on the sign up button
    wait_for_element(By.LINK_TEXT,
                     "Sign Up",
                     wait,
                     "Cannot find Sign Up Button").click()
    
    # Now we are at the sign up page.
    driver.implicitly_wait(wait_time)

    wait_for_element(By.ID,
                     "first_name",
                     wait,
                     "Cannot find First name field").send_keys(info['Firstname'])
        
    # Fill in necessary fields after observing first name field
    driver.find_element(By.ID,"last_name").send_keys(info['Lastname'])
    driver.find_element(By.ID, "email").send_keys(info['email'])
    driver.find_element(By.ID, "password").send_keys(info['password'])
    driver.find_element(By.ID, "password_confirm").send_keys(info['password'])
    
    # Get into the dashboard
    driver.find_element(By.ID, "signUpButton").click()
    
def verify_account(info,driver,ind_signup=True):
    """ 
    Verify bank account for 
    sending and receiving check 

    Assumptions:
    -successful signup
    -dashboard is loaded adequately
    
    Arguments:
    info -- dict of information for sender of check
    driver -- selenium webdriver instance
    ind_signup -- bool for signing up as individual

    """
    
    wait = WebDriverWait(driver,wait_time)
    driver.implicitly_wait(wait_time)
    
    wait_for_element(By.ID,
                     "updateProfile",
                     wait,
                     'Cannot find "Complete Profile" button').click()
                     
    driver.implicitly_wait(wait_time)

    # If doing an individual signup, use corresponding buttons    
    if ind_signup:

        wait_for_element(By.XPATH,
                         '//button[contains(text(),"Individual")]',
                         wait,
                         "Can't find 'Individual' button").click()

        verify_bank(wait,driver)
    
    # Filling out information for a business
    else:
    
        wait_for_element(By.XPATH,
                         '//button[contains(text(),"Business")]',
                         wait,
                         "Can't find 'Business' button").click()
                         
        driver.implicitly_wait(wait_time)
                         
        # Need to select corp drop down <TODO>
        
        wait_for_element(By.ID,
                         'business_name',
                         wait,
                         "No Business Name Field").send_keys(info['bus_name'])                                  

        wait_for_element(By.ID,
                         'website',
                         wait,
                         "No Website Field").send_keys(info['website'])                                  

        wait_for_element(By.ID,
                         'business_desc',
                         wait,
                         "No Business Description Field").send_keys(info['bus_desc'])

        # Need to select drop down for average payments

        wait_for_element(By.ID,
                         'tax_id',
                         wait,
                         "No Tax ID Field").send_keys(info['tax_id'])                                  
                                
        wait_for_element(By.ID,
                         'phone',
                         wait,
                         "No Phone Field").send_keys(info['phone'])

        wait_for_element(By.ID,
                         'legal_firstname',
                         wait,
                         "No Legal Firstname Field").send_keys(info['legal_first'])
                                 
        wait_for_element(By.ID,
                         'legal_lastname',
                         wait,
                         "No Legal Lastname Field").send_keys(info['legal_last'])
                         
        wait_for_element(By.ID,
                         'addressLine1',
                         wait,
                         "No Street Field").send_keys(info['street'])
        
        wait_for_element(By.ID,
                         'city',
                         wait,
                         "No City Field").send_keys(info['city'])
        
        wait_for_element(By.ID,
                         'state',
                         wait,
                         "No State Field").send_keys(info['state'])
                         
        wait_for_element(By.ID,
                         'addr_zip',
                         wait,
                         "No Zip Field").send_keys(info['zip'])
                         
        wait_for_element(By.ID,
                         'country',
                         wait,
                         "No Country Field").send_keys(info['country'])

        wait_for_element(By.XPATH,
                         '//button[contains(text(),"Activate!")]',
                         wait,
                         "Can't find 'Activate!' button").click()
                         
        verify_bank(wait,driver)
        

    
def send_check_dashboard(driver):
    """ 
    Get to the "Send a check" 
    dashboard
    
    Assumptions:
    -successful signup
    -dashboard is loaded adequately
    """
    driver.implicitly_wait(wait_time)
    # Go to the send a check dashboard
    driver.find_element(By.ID, "send_money").find_element_by_xpath('..').click()
    driver.find_element(By.LINK_TEXT,"Send a Check").click()
    
def fill_in_check_and_send(recipient_info,driver):
    """ 
    Input the check recipient 
    information and send 
    """
    driver.implicitly_wait(wait_time)
    # Input information on check fields
    driver.find_element(By.ID, 'email_id').send_keys(recipient_info['check_book_email'])
    driver.find_element(By.ID, 'receiverName').send_keys(recipient_info['whole_name'])
    driver.find_element(By.ID, 'amount').send_keys(recipient_info['amount'])
    driver.find_element(By.ID, 'description').send_keys(recipient_info['memo'])
    driver.find_element(By.ID, 'sendMoneyButton').click()
    driver.implicitly_wait(wait_time)
    # Click yes on the pop-down button
    button = driver.find_element(By.XPATH, 
                                 '//button[contains(text(),"Yes")]')
    button.click()
    time.sleep(sleep_time)
    
def confirm_email_for_check(recipient_info,driver):
    """ 
    Input the check recipient's 
    email to verify check 
    """
    # Check google email
    driver.implicitly_wait(wait_time)
    time.sleep(2*sleep_time)
    driver.get('https://www.gmail.com')
    driver.find_element(By.ID, 'Email').send_keys(recipient_info['email'])
    driver.find_element(By.ID, 'next').click()
    driver.find_element(By.ID, 'Passwd').send_keys(recipient_info['email_password'])
    driver.find_element(By.ID, 'signIn').click()

def print_or_deposit_online(recipient_info,driver,deposit_online=True):
    """ Print the received online check or deposit online """
    
    # Waiting for site to load
    time.sleep(2*sleep_time)
    driver.implicitly_wait(wait_time)
    wait = WebDriverWait(driver,wait_time)
    
    # Assuming the first email is the check email, check and click
    wait_for_element(By.CLASS_NAME,
                     'ts',
                     wait,
                     "Couldn't find First Email").click()
    
    # On the check page, click deposit online or print check
    time.sleep(sleep_time)

    # Choose to deposit online else print check    
    if deposit_online:
        
        deposit_button_one = wait_for_element(By.XPATH,
                                              '//img[contains(@src,"deposit_online_button.png")]/parent::a',
                                              wait,
                                              "Can't find deposit online button")
        deposit_button_one.click()
        driver.implicitly_wait(wait_time)        

        # Switch to pop-up window
        try:
            driver.switch_to_window(driver.window_handles[1])
        except:
            print "No new window appeared"

        deposit_button_two = wait_for_element(By.ID,
                                              'depositOnlineBtn',
                                              wait,
                                              "Can't find deposit online button")
        deposit_button_two.click()                 
        time.sleep(sleep_time)
        
        # Now choose the drop-down bar and bank

        choose_bank = wait_for_element(By.ID,
                                       'bank_name',
                                       wait,
                                       "No drop-down menu")        
                            
        choose_drop_down(choose_bank,'Wells Fargo',driver)

        wait_for_element(By.XPATH,
                         '//button[contains(text(),"Submit")]',
                         wait,
                         "No Submit Button").click()
                    
        driver.implicitly_wait(4*wait_time)

        wait_for_element(By.XPATH,
                         '//button[contains(text(),"Continue")]',
                         wait,
                         "No Continue Button").click()
    
        wait_for_element(By.ID,
                         "online_passcode",
                         wait,
                         "No passcode").send_keys(recipient_info['online_passcode'])
                         
        wait_for_element(By.ID,
                         "online_passcode_confirm",
                         wait,
                         "No passcode").send_keys(recipient_info['online_passcode'])
        
        xpath_btn_submit = '//*/button[@class="btn btn-danger"][@id="pinCreateBtn"]'
        try:
            wait_for_element(By.XPATH,
                             xpath_btn_submit,
                             wait,
                             "No Create Pin - Submit").click()
        except:
            wait_for_element(By.XPATH,
                             xpath_btn_submit,
                             wait,
                             "No Create Pin - Submit").click()

        xpath_btn_rec_check = '//*/button[@class="btn btn-success"][@id="sndCheckBtn"]'                         
        try:        
            wait_for_element(By.XPATH,
                             xpath_btn_rec_check,
                             wait,
                             "No Send Check Button").click()
        except:
            wait_for_element(By.XPATH,
                             xpath_btn_rec_check,
                             wait,
                             "No Send Check Button").click()           
    else:
        
        wait_for_element(By.XPATH,
                         '//img[contains(@src,"print_check_button.png")]/parent::a',
                         wait,
                         "Can't find print check button").click()
                
        driver.implicitly_wait(wait_time)        
        # Switch to pop-up window
        try:
            driver.switch_to_window(driver.window_handles[1])
        except:
            print "No new window appeared"
            
        wait_for_element(By.ID,
                         'acceptPrintCheck',
                         wait,
                         'No Print Check Button').click()
            
        wait_for_element(By.ID,
                         'willSavePDF',
                         wait,
                         'No Save PDF Button').click()  
                         
        wait_for_element(By.XPATH,'//button[contains(text(),"Got It!")]',
                         wait,
                         "Can't find 'Got it!' button").click()