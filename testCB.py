#!/usr/bin/python

# ---------------------------------------------------------------------------
# Author: Luis Alvarez
# File Description:
# This code creates a class template for
# testing checkbook.io and making sure
# checks can be sent or requested

# ---------------------------- Imports --------------------------------------
import integration_test_module as itm
from selenium import webdriver
# ---------------------------- Testing --------------------------------------

class testCB():
    """ 
    Class designed for testing 
    of UI for Checkbook 
    """        
    
    def test_SignUp_SendCheck_ReceiveCheck(self,
                                           driver,
                                           environment,
                                           ind_signup=True,
                                           send_check_ind=True,
                                           deposit_online=True):
        """ 
        Framework to test the following cases:

        Signup as Individual -> Send Check to Individual -> Deposit Online
        Signup as Business -> Send Check to Individual -> Deposit Online
        Signup as Individual -> Send Check to Business -> Deposit Online
        Signup as Business -> Send Check to Business -> Deposit Online
        Signup as Individual -> Send Check to Individual -> Print
        Signup as Business -> Send Check to Individual -> Print
        Signup as Individual -> Send Check to Business -> Print
        Signup as Business -> Send Check to Business -> Print

        Arguments:
        
        driver -- Selenium webdriver instance (Firefox or Chrome)
        ind_signup -- bool whether to signup as individual
                      (False denotes signup as business)
        send_check_ind -- bool indicating send check to individual
                          (False indicates send check to business)
        deposit_online -- bool indicating whether to deposit check
                          (False indicates to print check)
        """
        sender_info, recipient_info = itm.create_info(ind=ind_signup)
        
        itm.sign_up(sender_info,driver,environment)
        itm.verify_account(sender_info,driver,environment,ind_signup=ind_signup)
        itm.send_check_dashboard(driver)
        itm.fill_in_check_and_send_or_request(recipient_info,driver,
                                              ind=send_check_ind,send=True)
        itm.confirm_email_for_check(recipient_info,driver)
        itm.print_or_deposit_online(recipient_info,driver,
                                    deposit_online=deposit_online)
        
    def test_SignUp_RequestCheck(self,
                                 driver,
                                 environment,
                                 ind_signup=True,
                                 request_check_ind=True):
        """ 
        Framework to test the following cases:

        Signup as Individual -> Request Check from Individual
        Signup as Business -> Request Check from Individual
        Signup as Individual -> Request Check from Business
        Signup as Business -> Request Check from Business

        Arguments:
        
        driver -- Selenium webdriver instance (Firefox or Chrome)
        ind_signup -- bool whether to signup as individual
                      (False denotes signup as business)
        request_check_ind -- bool indicating request check from individual
                          (False indicates request from business)            
        """
        requester_info, payer_info = itm.create_info(ind=ind_signup)

        itm.sign_up(requester_info,driver,environment)
        itm.verify_account(requester_info,driver,environment,ind_signup=ind_signup)
        itm.request_check_dashboard(driver)
        itm.fill_in_check_and_send_or_request(payer_info,driver,
                                              ind=request_check_ind,send=False)
        itm.confirm_email_for_check(payer_info,driver)
        itm.send_check_from_invoice(payer_info,driver)
        
if __name__ == '__main__':
    
    # Instantiate test class
    test = testCB()    

    # Create a selenium webdriver
    wb = webdriver.Firefox()

    # Choose environment (or 'sandbox')
    environment = 'dev'
    
    # Signup as an individual
    ind_signup = True
    
    # Send check to individual
    send_check_ind = True
    
    # Deposit online 
    deposit_online = True
    
    test.test_SignUp_SendCheck_ReceiveCheck(wb,
                                            environment,
                                            ind_signup=ind_signup,
                                            send_check_ind=send_check_ind,
                                            deposit_online=deposit_online)
    # Request check from individual
    request_check_ind = True
 
    test.test_SignUp_RequestCheck(wb,
                                  environment,
                                  ind_signup=ind_signup,
                                  request_check_ind=request_check_ind)