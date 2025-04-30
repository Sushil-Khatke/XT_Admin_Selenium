from base_test import BaseTest
import time
from selenium.webdriver.common.by import By

class TestLogin(BaseTest):
    def __init__(self):
        super().__init__()
        self.base_url = "https://admin-qa.xstrela.com/sign-in"
        self.email = "xstrella@gmail.com"
        self.password = "Xstrella@123"

    def test_blank_form_submission(self):
        """Test submitting the form with empty fields"""
        try:
            print("\n=== Testing Blank Form Submission ===")
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Find and click submit button without entering any data
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit' or contains(text(), 'Login') or contains(text(), 'Sign in')]")
            submit_button.click()
            time.sleep(2)
            
            # Check for validation messages
            email_error = self.driver.find_elements(By.XPATH, "//input[@type='email']/following-sibling::div[contains(@class, 'error')]")
            password_error = self.driver.find_elements(By.XPATH, "//input[@type='password']/following-sibling::div[contains(@class, 'error')]")
            
            if email_error or password_error:
                print("✅ Validation messages displayed for empty fields")
                return True
            else:
                print("❌ No validation messages found for empty fields")
                return False
                
        except Exception as e:
            print(f"❌ Error in blank form test: {str(e)}")
            return False

    def test_invalid_credentials(self):
        """Test login with invalid email and password"""
        try:
            print("\n=== Testing Invalid Credentials ===")
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Enter invalid credentials
            email_field = self.wait_for_element("//input[@type='email' or @name='email']")
            email_field.clear()
            self.type_slowly(email_field, "invalid@email.com")
            
            password_field = self.driver.find_element(By.XPATH, "//input[@type='password' or @name='password']")
            password_field.clear()
            self.type_slowly(password_field, "wrongpassword")
            
            # Submit form
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit' or contains(text(), 'Login') or contains(text(), 'Sign in')]")
            submit_button.click()
            time.sleep(3)
            
            # Check for error message
            error_message = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'error') or contains(text(), 'Invalid') or contains(text(), 'incorrect')]")
            
            if error_message:
                print("✅ Error message displayed for invalid credentials")
                return True
            else:
                print("❌ No error message found for invalid credentials")
                return False
                
        except Exception as e:
            print(f"❌ Error in invalid credentials test: {str(e)}")
            return False

    def test_input_validation(self):
        """Test various input validations"""
        try:
            print("\n=== Testing Input Field Validations ===")
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Test invalid email format
            email_field = self.wait_for_element("//input[@type='email' or @name='email']")
            email_field.clear()
            self.type_slowly(email_field, "invalid-email")
            email_field.send_keys("\t")  # Tab out to trigger validation
            
            time.sleep(1)
            email_error = self.driver.find_elements(By.XPATH, "//input[@type='email']/following-sibling::div[contains(@class, 'error')]")
            
            if email_error:
                print("✅ Email format validation working")
            else:
                print("❌ Email format validation not working")
            
            # Test password minimum length
            password_field = self.driver.find_element(By.XPATH, "//input[@type='password' or @name='password']")
            password_field.clear()
            self.type_slowly(password_field, "short")
            password_field.send_keys("\t")  # Tab out to trigger validation
            
            time.sleep(1)
            password_error = self.driver.find_elements(By.XPATH, "//input[@type='password']/following-sibling::div[contains(@class, 'error')]")
            
            if password_error:
                print("✅ Password length validation working")
            else:
                print("❌ Password length validation not working")
            
            return True
                
        except Exception as e:
            print(f"❌ Error in input validation test: {str(e)}")
            return False

    def test_login_validation(self):
        try:
            # Navigate to the admin website
            self.driver.get(self.base_url)
            time.sleep(5)
            
            print("\n=== Testing Login Form ===")
            
            # Check form elements
            print("\n1. Checking Form Elements:")
            try:
                # Email field
                email_field = self.wait_for_element("//input[@type='email' or @name='email']")
                print(f"✅ Email field found")
                email_field.clear()
                self.type_slowly(email_field, self.email)
                print("✅ Email entered")
            except:
                print("❌ Email field not found")
                return False
            
            try:
                # Password field
                password_field = self.driver.find_element(By.XPATH, "//input[@type='password' or @name='password']")
                print(f"✅ Password field found")
                password_field.clear()
                self.type_slowly(password_field, self.password)
                print("✅ Password entered")
            except:
                print("❌ Password field not found")
                return False
            
            # Submit login form
            try:
                submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit' or contains(text(), 'Login') or contains(text(), 'Sign in')]")
                submit_button.click()
                print("✅ Login form submitted")
            except:
                print("❌ Submit button not found")
                return False
            
            # Wait for login to complete and verify
            time.sleep(5)
            try:
                # Check for successful login by looking for dashboard or welcome message
                success_element = self.wait_for_element("//*[contains(text(), 'Welcome') or contains(text(), 'Dashboard')]")
                print("✅ Login successful")
                print(f"   Redirected to: {self.driver.current_url}")
                
                # Check for "Activity Dashboard" text
                try:
                    activity_dashboard = self.wait_for_element("//*[contains(text(), 'Activity Dashboard')]")
                    print("✅ 'Activity Dashboard' text found on the page")
                    return True
                except:
                    print("❌ 'Activity Dashboard' text not found on the page")
                    return False
            except:
                print("❌ Login failed - Could not verify successful login")
                return False
                
        except Exception as e:
            print(f"❌ Error during login test: {str(e)}")
            return False

    def test_login_and_return_driver(self):
        """Login and return the driver for use in other tests"""
        try:
            self.driver.get(self.base_url)
            time.sleep(5)
            
            email_field = self.wait_for_element("//input[@type='email' or @name='email']")
            email_field.clear()
            self.type_slowly(email_field, self.email)
            
            password_field = self.driver.find_element(By.XPATH, "//input[@type='password' or @name='password']")
            password_field.clear()
            self.type_slowly(password_field, self.password)
            
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit' or contains(text(), 'Login') or contains(text(), 'Sign in')]")
            submit_button.click()
            
            time.sleep(5)
            return self.driver
            
        except Exception as e:
            print(f"❌ Error during login: {str(e)}")
            return None
            
        finally:
            self.close() 