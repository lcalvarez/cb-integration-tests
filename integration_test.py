#!/usr/bin/python

# ---------------------------------------------------------------------------
# Author: Luis Alvarez
# File Description

# Imports -------------------------------------------------------------------
from selenium import webdriver
import integration_test_module as itm
import unittest

#---------------------------- Testing ---------------------------------------
class TestCB(unittest.TestCase):
    """ 
    Class designed for testing 
    of UI for Checkbook 
    """
    
    # <TODO> To assert or not to assert?
                                    
    def test_SignUp_Bus_Send_Ind_ReceiveCheck_Deposit(self):
        """ 
        Sign up as a business,
        send check to individual,
        receive check,
        deposit online
        """
        driver = webdriver.Firefox()
        sender_info, recipient_info = itm.create_info(ind=False)
        
        itm.sign_up(sender_info,driver)
        itm.verify_account(sender_info,driver,ind_signup=False)
        itm.send_check_dashboard(driver)
        itm.fill_in_check_and_send(recipient_info,driver)
        itm.confirm_email_for_check(recipient_info,driver)
        itm.print_or_deposit_online(recipient_info,driver,
                                    deposit_online=True)
        driver.close()
                                    
    def test_SignUp_Ind_Send_Ind_ReceiveCheck_Deposit(self):
        """ 
        Sign up as an individual,
        send check to individual,
        receive check,
        deposit online
        """
        driver = webdriver.Firefox()
        sender_info, recipient_info = itm.create_info(ind=True)
        
        itm.sign_up(sender_info,driver)
        itm.verify_account(sender_info,driver,ind_signup=True)
        itm.send_check_dashboard(driver)
        itm.fill_in_check_and_send(recipient_info,driver)
        itm.confirm_email_for_check(recipient_info,driver)
        itm.print_or_deposit_online(recipient_info,driver,
                                    deposit_online=True)
        driver.close()
        
    def test_SignUp_Bus_Send_Bus_ReceiveCheck_Deposit(self):
        pass
    
    def test_SignUp_Ind_Send_Bus_ReceiveCheck_Deposit(self):
        pass
    
    # 4 Replicates with print check?
    
    
    # Request checks now
        
    def test_SignUp_Ind_RequestCheck(self):
        pass
    
    def test_SignUp_Bus_RequestCheck(self):
        pass
    
if __name__ == '__main__':
    unittest.main()    