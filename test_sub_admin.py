from base_test import BaseTest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

class TestSubAdmin(BaseTest):
    def __init__(self):
        super().__init__()
        self.base_url = "https://admin-qa.xstrela.com/sign-in"
        self.sub_admin_url = "https://admin-qa.xstrela.com/sub-admin"
        self.email = "xstrella@gmail.com"
        self.password = "Xstrella@123"

    def login_and_navigate_to_sub_admin(self):
        """Login and navigate to Sub Admin section"""
        try:
            print("\n=== Navigating to Sub Admin Section ===")
            
            # First login
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Login process
            email_field = self.wait_for_element("//input[@type='email' or @name='email']")
            email_field.clear()
            self.type_slowly(email_field, self.email)
            
            password_field = self.driver.find_element(By.XPATH, "//input[@type='password' or @name='password']")
            password_field.clear()
            self.type_slowly(password_field, self.password)
            
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            time.sleep(5)
            
            # Verify successful login
            activity_dashboard = self.wait_for_element("//*[contains(text(), 'Activity Dashboard')]")
            print("✅ Successfully logged in")
            
            # Navigate directly to Sub Admin URL
            self.driver.get(self.sub_admin_url)
            time.sleep(5)  # Increased wait time
            print(f"✅ Navigated to Sub Admin URL: {self.sub_admin_url}")
            
            # Take a screenshot for debugging
            self.driver.save_screenshot("sub_admin_page.png")
            print("✅ Screenshot saved as sub_admin_page.png")
            
            # Print current URL for debugging
            print(f"Current URL: {self.driver.current_url}")
            
            # Verify we're on the correct page
            try:
                # Check for Sub Admin header with count (more flexible XPath)
                sub_admin_header = self.wait_for_element("//*[contains(text(), 'Sub Admin') or contains(text(), 'Sub-Admin')]")
                print("✅ Found Sub Admin header")
                print(f"   Header text: {sub_admin_header.text}")
                
                # Check for Create New Sub-Admin button (more flexible XPath)
                create_button = self.wait_for_element("//button[contains(text(), 'Create') and contains(text(), 'Sub')]")
                print("✅ Found Create New Sub-Admin button")
                print(f"   Button text: {create_button.text}")
                
                return True
                
            except Exception as e:
                print(f"❌ Error verifying Sub Admin page elements: {str(e)}")
                print("Current page source:")
                print(self.driver.page_source[:1000])  # Print more of the page source
                return False
                
        except Exception as e:
            print(f"❌ Error during navigation: {str(e)}")
            return False

    def verify_sub_admin_elements(self):
        """Verify the presence of key elements on the Sub Admin page"""
        try:
            print("\n=== Verifying Sub Admin Page Elements ===")
            time.sleep(5)  # Increased wait time for all elements to load
            
            # List of expected elements to verify with more flexible XPaths
            elements_to_verify = [
                ("Sub Admin title", "//*[contains(text(), 'Sub Admin') or contains(text(), 'Sub-Admin')]"),
                ("Create New Sub-Admin button", "//button[contains(text(), 'Create') and contains(text(), 'Sub')]"),
                ("User Name header", "//*[contains(text(), 'User') and contains(text(), 'Name')]"),
                ("Email header", "//*[contains(text(), 'Email')]"),
                ("Enable/Disable header", "//*[contains(text(), 'Enable') or contains(text(), 'Disable')]"),
                ("Action header", "//*[contains(text(), 'Action')]"),
                ("Super Admin user", "//*[contains(text(), 'xstrela')]"),
                ("Enable/Disable toggle", "//input[@type='checkbox'] | //div[contains(@class, 'toggle')] | //div[contains(@class, 'switch')]"),
                ("Delete action button", "//button[contains(@class, 'delete')] | //button[contains(@class, 'trash')] | //button[contains(@title, 'Delete')]")
            ]
            
            for element_name, xpath in elements_to_verify:
                try:
                    element = self.wait_for_element(xpath, timeout=5)  # Increased timeout
                    print(f"✅ {element_name} found")
                    print(f"   Element text: {element.text if element.text else '[No text - likely a button/input]'}")
                except Exception as e:
                    print(f"❌ {element_name} not found")
                    print(f"   Error: {str(e)}")
                    print(f"   XPath used: {xpath}")
                    return False
            
            print("✅ All Sub Admin page elements verified")
            return True
                
        except Exception as e:
            print(f"❌ Error while verifying Sub Admin elements: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all Sub Admin related tests"""
        try:
            # Navigate to Sub Admin section
            if not self.login_and_navigate_to_sub_admin():
                return False
                
            # Verify Sub Admin page elements
            if not self.verify_sub_admin_elements():
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error in Sub Admin tests: {str(e)}")
            return False
            
        finally:
            self.close() 