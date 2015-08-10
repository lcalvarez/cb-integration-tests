#!/usr/bin/python

# ---------------------------------------------------------------------------
# Author: Luis Alvarez
# File Description

# Imports -------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import unittest
import random
import string
import time
import ipdb

# <TODO> Docstring definition assumptions and arguments.

# Globals for waiting in between 
wait_time = 20
sleep_time = 5

# Functions
def id_generator(size=6, chars=string.ascii_letters + string.digits):
    """ Returns a random combination of characters. """
    return ''.join(random.choice(chars) for _ in range(size))

def sign_up(info,driver):
    """ Sign up using info and browser 
    and get to the dashboard """    
    
    # Move to home page
    base_url = "https://dev.checkbook.io"
    driver.get(base_url)
    
    # Wait for page to load
    time.sleep(sleep_time)
    wait = WebDriverWait(driver,wait_time)
    driver.implicitly_wait(2*wait_time)
    
    # Click on the sign up button
    try:
        sign_up = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up")))
    except:
        print "Cannot find sign up."
    sign_up.click()
    
    # Now we are at the sign up page.
    driver.implicitly_wait(wait_time)
    try:
        first_name = wait.until(EC.element_to_be_clickable((By.ID, "first_name")))
    except:
        print "Cannot find first name"
        
    # Fill in necessary fields
    first_name.send_keys(info["Firstname"])
    driver.find_element(By.ID,"last_name").send_keys(info['Lastname'])
    driver.find_element(By.ID, "email").send_keys(info['email'])
    driver.find_element(By.ID, "password").send_keys(info['password'])
    driver.find_element(By.ID, "password_confirm").send_keys(info['password'])
    # Get into the dashboard
    driver.find_element(By.ID, "signUpButton").click()
    
def verify_account(info,driver):
    """ Verify bank account for sending and receiving check """
    wait = WebDriverWait(driver,wait_time)
    driver.implicitly_wait(wait_time)
    
    try:
        complete_profile = wait.until(EC.element_to_be_clickable((By.ID, "updateProfile")))
    except:
        print "Cannot find Complete Profile."
        return
    complete_profile.click()
    driver.implicitly_wait(wait_time)
    
    try:
        individual_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Individual")]')))
    except:
        print "Can't find individual button"
    individual_button.click()
    driver.implicitly_wait(wait_time); time.sleep(sleep_time) 
    
    try:
        verify_bank = wait.until(EC.element_to_be_clickable((By.ID, 'addUpdateButton')))
    except:
        print "Can't find Verify My Bank button"
    verify_bank.click()
    driver.implicitly_wait(wait_time); time.sleep(sleep_time)
    
    try:
        choose_bank = wait.until(EC.element_to_be_clickable((By.ID, "bank_name")))
    except:
        print "No drop-down menu"

    select = Select(choose_bank)
    select.select_by_visible_text("Wells Fargo")
    driver.find_element(By.ID, "bank_user").send_keys(info['bank_username'])
    driver.find_element(By.ID, "bank_passwd").send_keys(info['bank_password'])
    driver.implicitly_wait(4*wait_time); time.sleep(sleep_time)

    try:
        driver.find_element(By.XPATH, '//button[contains(text(),"Submit")]').click()    
    except:
        print "No Submit Button"
        
    driver.implicitly_wait(4*wait_time)

    try:
        driver.find_element(By.XPATH, '//button[contains(text(),"Complete")]').click()
    except:
        print "No Complete Button"
    
    time.sleep(sleep_time)
    driver.implicitly_wait(4*wait_time)    
    
def send_check_dashboard(driver):
    """ Get to the send a check dashboard """
    driver.implicitly_wait(wait_time)
    # Go to the send a check dashboard
    driver.find_element(By.ID, "send_money").find_element_by_xpath('..').click()
    driver.find_element(By.LINK_TEXT,"Send a Check").click()
    
def fill_in_check_and_send(recipient_info,driver):
    """ Input the check recipient information and send """
    driver.implicitly_wait(wait_time)
    # Input information on check fields
    driver.find_element(By.ID, 'email_id').send_keys(recipient_info['email'])
    driver.find_element(By.ID, 'receiverName').send_keys(recipient_info['whole_name'])
    driver.find_element(By.ID, 'amount').send_keys(recipient_info['amount'])
    driver.find_element(By.ID, 'description').send_keys(recipient_info['memo'])
    driver.find_element(By.ID, 'sendMoneyButton').click()
    driver.implicitly_wait(wait_time)
    # Click yes on the pop-down button
    button = driver.find_element(By.XPATH, '//button[contains(text(),"Yes")]')
    button.click()
    time.sleep(sleep_time)
    
def confirm_email_for_check(recipient_info,driver):
    """ Input the check recipient's email to verify check """
    # Check google email
    driver.implicitly_wait(wait_time)
    time.sleep(sleep_time)
    driver.get('https://www.gmail.com')
    driver.find_element(By.ID, 'Email').send_keys(recipient_info['email'])
    driver.find_element(By.ID, 'next').click()
    driver.find_element(By.ID, 'Passwd').send_keys(recipient_info['email_password'])
    driver.find_element(By.ID, 'signIn').click()

def print_or_deposit_online(recipient_info,driver,deposit_online=True):
    """ Print the received online check or deposit online """
    
    # Waiting for site
    time.sleep(sleep_time)
    driver.implicitly_wait(wait_time)
    wait = WebDriverWait(driver,2*wait_time)
    
    # Assuming the first email is the check email, check and click
    try:
        email = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ts')))
    except:
        email = driver.find_element(By.CLASS_NAME, 'ts') 
    email.click()
    
    # On the check page, click deposit online or print check
    time.sleep(sleep_time)    
    if deposit_online:
        try:
            deposit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//img[contains(@src,"deposit_online_button.png")]/parent::a')))
        except:
            print "Can't find deposit online button"
        deposit_button.click()
        
        driver.implicitly_wait(wait_time)        
        # Switch to pop-up window
        try:
            driver.switch_to_window(driver.window_handles[1])
        except:
            print "No new window appeared"
            
        try:
            deposit_button = wait.until(EC.element_to_be_clickable((By.ID, 'depositOnlineBtn')))
        except:
            print "Can't find deposit online button"
        deposit_button.click()            
            
        time.sleep(sleep_time)
        
        # Now choose the drop-down bar and bank
                        
        try:
            choose_bank = wait.until(EC.element_to_be_clickable((By.ID, "bank_name")))
        except:
            print "No drop-down menu"
    
        select = Select(choose_bank)
        select.select_by_visible_text("Wells Fargo")
        driver.find_element(By.ID, "bank_user").send_keys('plaid_test')
        driver.find_element(By.ID, "bank_passwd").send_keys('plaid_good')
        driver.implicitly_wait(4*wait_time); time.sleep(sleep_time)
        
        try:
            driver.find_element(By.XPATH, '//button[contains(text(),"Submit")]').click()    
        except:
            print "No Submit Button"
            
        driver.implicitly_wait(4*wait_time)
    
        try:
            driver.find_element(By.XPATH, '//button[contains(text(),"Continue")]').click()
        except:
            print "No Continue Button"
            
        try:
            wait.until(EC.element_to_be_clickable((By.ID, "online_passcode"))).send_keys(recipient_info['online_passcode'])
            wait.until(EC.element_to_be_clickable((By.ID, "online_passcode_confirm"))).send_keys(recipient_info['online_passcode'])
        except:
            print "No passcode"
            
        try:
            wait.until(EC.element_to__clickable((By.ID, 'pinCreateBtn'))).click()    
        except:
            print "No Submit Button"
        
        try:
            wait.until(EC.element_to__clickable((By.ID, 'sndEnterAcctNumButton'))).click()    
        except:
            print "No EnterAcct Button"

        try:
            wait.until(EC.element_to__clickable((By.ID, 'sendCheckBtn'))).click()    
        except:
            print "No EnterAcct Button"
            
            
        # Done
            
    else:
        try:
            print_check_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//img[contains(@src,"print_check_button.png")]/parent::a')))
        except:
            print "Can't find print check button"
        print_check_button.click()

        
        
        
   
def test_gmail():
    driver = webdriver.Firefox()
    
    sender_info = {'Firstname':'test-first'+id_generator(3),
                   'Lastname':'test-last'+id_generator(3),
                   'email':'testcb72+'+id_generator()+'@gmail.com',
                   'password':id_generator(),
                   'bank_username':'plaid_test',
                   'bank_password':'plaid_good'}

    
    recipient_info = {'email':'testcb72@gmail.com',
                      'whole_name':'TestFirst TestLast',
                      'amount':str(random.randint(1,10)),
                      'memo':'Automated Test',
                      'email_password':'0o9i8u7y',
                      'online_passcode':id_generator()}

    confirm_email_for_check(recipient_info,driver)
    print_or_deposit_online(recipient_info,driver)
    

#---------------------------- Testing ---------------------------------------


class TestRegexMatches(unittest.TestCase):
    """ Class designed for testing of UI for Checkbook """
    
    # <TODO> To assert or not to assert?
    
    def setUp(self):
        # Use firefox
        self.driver = webdriver.Firefox()
    
    def test_SignUp_ReceiveCheck_Deposit(self):
        """ Make sure one can sign up """
        
        sender_info = {'Firstname':'test-first'+id_generator(3),
                       'Lastname':'test-last'+id_generator(3),
                       'email':'testcb72+'+id_generator()+'@gmail.com',
                       'password':id_generator(),
                       'bank_username':'plaid_test',
                       'bank_password':'plaid_good'}
                     
        recipient_info = {'email':'testcb72@gmail.com',
                          'whole_name':'TestFirst TestLast',
                          'amount':str(random.randint(1,10)),
                          'memo':'Automated Test',
                          'email_password':'0o9i8u7y',
                          'online_passcode':id_generator()}
        
        sign_up(sender_info,self.driver)
        verify_account(sender_info,self.driver)
        send_check_dashboard(self.driver)
        fill_in_check_and_send(recipient_info,self.driver)
        confirm_email_for_check(recipient_info,self.driver)
        print_or_deposit_online(recipient_info,self.driver,
                                deposit_online=True)        
        
if __name__ == '__main__':
    unittest.main()    