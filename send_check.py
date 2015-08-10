#!/usr/bin/python

# -----------------------------------------------------
# Author: Luis Alvarez
# This is a simple test for using the Selenium Webdrive

# Imports
from selenium import webdriver

# Testing

sender_usrname = 'testcb72+Business@gmail.com'
sender_pswrd = 'zuqs4138'

recip_usrname =  'testcb72+Individual@gmail.com'
recip_pswrd = 'zuqs4138'

# First page
driver = webdriver.Firefox()
driver.get("https://dev.checkbook.io")
driver.implicitly_wait(10) # 10 seconds
assert "Checkbook.io" in driver.title
log_on = driver.find_element_by_link_text('Login')
log_on.click()

# Logging in
username = driver.find_element_by_id('senders_email_id')
username.send_keys(sender_usrname)
passwrd = driver.find_element_by_id('online_passcode')
passwrd.send_keys(sender_pswrd)
logon_button = driver.find_element_by_id('loginCheck')
logon_button.click()
driver.implicitly_wait(10) # seconds

# Dashboard
parent = driver.find_element_by_id('send_money').find_element_by_xpath('..').click()
send_check = driver.find_element_by_link_text('Send a Check').click()
driver.implicitly_wait(10) # seconds

# Send Check
email = driver.find_element_by_id('email_id').send_keys(recip_usrname)
name = driver.find_element_by_id('receiverName').send_keys('IndFirst IndLast')
amount = driver.find_element_by_id('amount').send_keys('1.00')
memo = driver.find_element_by_id('description').send_keys('Automated Tests')
driver.find_element_by_id('sendMoneyButton').click()
driver.implicitly_wait(10) # seconds
button = driver.find_element_by_xpath('//button[contains(text(),"Yes")]')
button.click()

# Check google email
driver.get('https://www.gmail.com')
driver.find_element_by_id('Email').send_keys('testcb72@gmail.com')
driver.find_element_by_id('next').click()
driver.find_element_by_id('Passwd').send_keys('1k8L09ht')
driver.find_element_by_id('signIn').click()
