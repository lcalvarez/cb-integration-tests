#!/usr/bin/python

# ---------------------------------------------------------------------------
# Author: Luis Alvarez
# File Description
# This script is  driver for
# implementing the tests in testCB
# using a command line interface

# ---------------------------- Imports --------------------------------------
from selenium import webdriver
import testCB as tCB

def main():
    
    def choose(init_prompt,error_prompt,type_one,type_two):
        return_str = raw_input(init_prompt)
        while return_str.lower() not in [type_one.lower(), type_two.lower()]:
            return_str = raw_input(error_prompt)
        return return_str
    
    type_transact = choose("\nSend or Request a Check?\nPlease input Send or Request: ",
                           "\nPlease input an appropriate transaction\nSend or Request: ",
                           'Send','Request')
                           
    signup_str = choose("\nWould you like to sign up as an Individual or a Business?\nPlease input Ind or Bus: ",
                        "\nPlease choose an appropriate type\nInd or Bus: ",
                        'ind','bus')
                        
    recipient_type = choose("\nWould you like the recipient to be an Individual or a Business?\nPlease input Ind or Bus: ",
                            "\nPlease choose an appropriate type\nInd or Bus: ",
                            'ind','bus')
                           
    if type_transact == 'Send':
        deposit_or_print = choose ("\nWould you like to Deposit Online or Print Check?\nPlease input Deposit or Print: ",
                                   "\nPlease input an appropriate type\nDeposit or Print: ",
                                   'Deposit','Print')
                           
    environment = choose("\nWhich environment would you like to test on?\nPlease input dev or sandbox: ",
                         "\nPlease input an appropriate environment\ndev or sandbox: ",
                         'dev','sandbox')

    if environment.lower() == 'sandbox':
        environment = 'www'

    driver = raw_input("\nPlease choose a web browser\nFirefox, Chrome, or Safari: ")
    while driver.lower() not in ['Firefox'.lower(), 'Chrome'.lower(), 'Safari'.lower()]:
        driver = raw_input("\nPlease choose an appropriate type of brower\nFirefox, Chrome, or Safari: ")
        
    test = tCB.testCB()
    
    if driver.lower() == 'firefox':
        wb =  webdriver.Firefox()
    elif driver.lower() == 'chrome':
        wb = webdriver.Chrome()
    elif driver.lower() == 'safari':
        wb = webdriver.Safari()
        
    if signup_str.lower() == 'ind':
        ind_signup = True
    else:
        ind_signup = False
    
    if type_transact == 'Send':

            
        if recipient_type.lower() == 'ind':
            send_check_ind = True
        else:
            send_check_ind = False
        
        if deposit_or_print.lower() == 'deposit':
            deposit_online = True
        else:
            deposit_online = False
        
        test.test_SignUp_SendCheck_ReceiveCheck(wb,
                                                environment,
                                                ind_signup=ind_signup,
                                                send_check_ind=send_check_ind,
                                                deposit_online=deposit_online)
        
    else:
        
        if recipient_type.lower() == 'ind':
            request_check_ind = True
        else:
            request_check_ind = False
        
        test.test_SignUp_RequestCheck(wb,
                                      environment,
                                      ind_signup=ind_signup,
                                      request_check_ind=request_check_ind)
                                                
if __name__ == '__main__':
    main()