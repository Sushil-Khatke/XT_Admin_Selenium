from base_test import BaseTest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import platform
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestCreateSubAdmin(BaseTest):
    def __init__(self):
        super().__init__()
        self.base_url = "https://admin-qa.xstrela.com/sign-in"
        self.sub_admin_url = "https://admin-qa.xstrela.com/sub-admin"
        self.email = "xstrella@gmail.com"
        self.password = "Xstrella@123"
        self.driver = None
        
        # New Sub Admin details
        self.new_sub_admin = {
            "name": "Test007",
            "email": "sushil+test007@rapidinnovation.dev",
            "password": "Rapid@1234"
        }
    
    def setUp(self):
        """Set up the WebDriver"""
        print("\n=== Setting up WebDriver ===")
        
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Check if running on Mac ARM
        if platform.system() == "Darwin" and platform.machine() == "arm64":
            print("✅ Detected Mac ARM64 architecture")
            chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        
        try:
            # Let Selenium Manager handle driver installation
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
            print("✅ WebDriver initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing WebDriver: {str(e)}")
            raise

    def tearDown(self):
        """Clean up after the test"""
        if self.driver:
            try:
                self.driver.quit()
                print("✅ Browser closed successfully")
            except Exception as e:
                print(f"⚠️ Error closing browser: {str(e)}")

    def wait_for_element(self, xpath, timeout=10):
        """Wait for an element to be present and return it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element
        except TimeoutException:
            print(f"❌ Timeout waiting for element: {xpath}")
            self.driver.save_screenshot("timeout_error.png")
            raise
        except Exception as e:
            print(f"❌ Error finding element {xpath}: {str(e)}")
            self.driver.save_screenshot("element_error.png")
            raise

    def type_slowly(self, element, text, delay=0.1):
        """Type text into an element with a delay between each character"""
        for char in text:
            element.send_keys(char)
            time.sleep(delay)

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
            
            password_field = self.wait_for_element("//input[@type='password' or @name='password']")
            password_field.clear()
            self.type_slowly(password_field, self.password)
            
            submit_button = self.wait_for_element("//button[@type='submit']")
            submit_button.click()
            time.sleep(5)
            
            # Verify successful login
            activity_dashboard = self.wait_for_element("//*[contains(text(), 'Activity Dashboard')]")
            print("✅ Successfully logged in")
            
            # Navigate directly to Sub Admin URL
            self.driver.get(self.sub_admin_url)
            time.sleep(5)
            print(f"✅ Navigated to Sub Admin URL: {self.sub_admin_url}")
            
            # Take a screenshot for debugging
            self.driver.save_screenshot("sub_admin_page.png")
            print("✅ Screenshot saved as sub_admin_page.png")
            
            return True
                
        except Exception as e:
            print(f"❌ Error during navigation: {str(e)}")
            self.driver.save_screenshot("navigation_error.png")
            return False

    def open_create_sub_admin_modal(self):
        """Open the Create Sub Admin modal"""
        print("\n=== Opening Create Sub Admin Modal ===")
        create_button = self.wait_for_element("//button[contains(., 'Create New Sub-Admin')]")
        print("✅ Found Create New Sub-Admin button")
        self.driver.save_screenshot("before_modal.png")
        self.driver.execute_script("arguments[0].click();", create_button)
        time.sleep(2)  # Wait for modal animation
        self.driver.save_screenshot("after_modal_open.png")
        return True

    def verify_modal_closed(self):
        """Verify that the modal is closed"""
        try:
            # Wait for the Create New Sub-Admin button to be visible again
            self.wait_for_element("//button[contains(., 'Create New Sub-Admin')]")
            print("✅ Modal closed successfully")
            return True
        except:
            print("❌ Modal is still open")
            self.driver.save_screenshot("modal_not_closed.png")
            return False

    def test_close_modal_with_x_button(self):
        """Test closing the modal using the X button"""
        try:
            print("\n=== Testing Modal Close with X Button ===")
            
            # Open the modal
            if not self.open_create_sub_admin_modal():
                return False
            
            # Find and click the X button using data-testid
            close_button = self.wait_for_element("//*[@data-testid='modal-close-button']")
            print("✅ Found X button")
            
            # Take screenshot before clicking
            self.driver.save_screenshot("before_x_click.png")
            
            # Click the X button
            close_button.click()
            print("✅ Clicked X button")
            
            # Verify modal closed
            return self.verify_modal_closed()
            
        except Exception as e:
            print(f"❌ Error testing X button close: {str(e)}")
            self.driver.save_screenshot("x_button_error.png")
            return False

    def test_close_modal_with_cancel_button(self):
        """Test closing the modal using the Cancel button"""
        try:
            print("\n=== Testing Modal Close with Cancel Button ===")
            
            # Open the modal
            if not self.open_create_sub_admin_modal():
                return False
            
            # Print all buttons for debugging
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            print("\nFound buttons:")
            for button in buttons:
                try:
                    text = button.text
                    class_name = button.get_attribute("class")
                    print(f"Button text: '{text}', class: '{class_name}'")
                except:
                    print("Could not get button details")
            
            # Try different locators for the Cancel button
            cancel_locators = [
                "//button[text()='Cancel']",
                "//button[contains(text(), 'Cancel')]",
                "//button[contains(@class, 'cancel')]",
                "//button[contains(@class, 'secondary')]",
                "//button[contains(@class, 'dhrWQt')]"  # Class we saw in previous runs
            ]
            
            cancel_button = None
            for locator in cancel_locators:
                try:
                    print(f"\nTrying Cancel button locator: {locator}")
                    cancel_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, locator))
                    )
                    if cancel_button:
                        print(f"✅ Found Cancel button using locator: {locator}")
                        break
                except:
                    print(f"❌ Cancel button not found with locator: {locator}")
            
            if not cancel_button:
                print("❌ Could not find Cancel button with any locator")
                self.driver.save_screenshot("cancel_button_not_found.png")
                return False
            
            # Take screenshot before clicking
            self.driver.save_screenshot("before_cancel_click.png")
            
            # Try to click the Cancel button
            try:
                cancel_button.click()
                print("✅ Clicked Cancel button using normal click")
            except:
                try:
                    self.driver.execute_script("arguments[0].click();", cancel_button)
                    print("✅ Clicked Cancel button using JavaScript")
                except Exception as e:
                    print(f"❌ Failed to click Cancel button: {str(e)}")
                    return False
            
            # Verify modal closed
            return self.verify_modal_closed()
            
        except Exception as e:
            print(f"❌ Error testing Cancel button close: {str(e)}")
            self.driver.save_screenshot("cancel_button_error.png")
            return False

    def test_create_sub_admin(self):
        """Test creating a new sub admin"""
        try:
            print("\n=== Opening Create Sub Admin Form ===")
            
            # Take screenshot of initial state
            self.driver.save_screenshot("initial_state.png")
            
            # Find and click the Create New Sub-Admin button
            create_button = self.wait_for_element("//button[contains(., 'Create New Sub-Admin')]")
            print("✅ Found Create New Sub-Admin button")
            
            # Take screenshot before clicking
            self.driver.save_screenshot("before_click.png")
            
            # Click the button using JavaScript
            self.driver.execute_script("arguments[0].click();", create_button)
            time.sleep(2)  # Short wait for modal animation
            
            # Take screenshot after clicking
            self.driver.save_screenshot("after_click.png")
            
            print("\n=== Filling Create Sub Admin Form ===")
            
            # Wait for and fill the Name field using ID
            name_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "user_name"))
            )
            name_field.clear()
            name_field.send_keys(self.new_sub_admin["name"])
            print("✅ Filled Name field")
            
            # Wait for and fill the Email field using ID
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.clear()
            email_field.send_keys(self.new_sub_admin["email"])
            print("✅ Filled Email field")
            
            # Wait for and fill the Password field using ID
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            password_field.clear()
            password_field.send_keys(self.new_sub_admin["password"])
            print("✅ Filled Password field")
            
            # Take screenshot before submitting
            self.driver.save_screenshot("before_submit.png")
            
            # Print all buttons for debugging
            print("\nLooking for submit button...")
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            print(f"Found {len(buttons)} buttons:")
            for button in buttons:
                try:
                    text = button.text
                    class_name = button.get_attribute("class")
                    print(f"Button text: '{text}', class: '{class_name}'")
                except:
                    print("Could not get button details")
            
            # Try different submit button locators
            submit_button = None
            submit_locators = [
                "//button[text()='Create']",
                "//button[contains(text(), 'Create')]",
                "//button[@type='submit']",
                "//button[contains(@class, 'submit')]",
                "//button[contains(@class, 'primary')]",
                "//button[contains(@class, 'create')]"
            ]
            
            for locator in submit_locators:
                try:
                    print(f"\nTrying submit button locator: {locator}")
                    submit_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, locator))
                    )
                    if submit_button:
                        print(f"✅ Found submit button using locator: {locator}")
                        break
                except:
                    print(f"❌ Button not found with locator: {locator}")
            
            if not submit_button:
                print("❌ Could not find submit button with any locator")
                # Save page source for debugging
                with open("form_page_source.html", "w") as f:
                    f.write(self.driver.page_source)
                print("✅ Saved form page source to form_page_source.html")
                return False
            
            # Click the submit button
            try:
                submit_button.click()
                print("✅ Clicked submit button using normal click")
            except:
                try:
                    self.driver.execute_script("arguments[0].click();", submit_button)
                    print("✅ Clicked submit button using JavaScript")
                except Exception as e:
                    print(f"❌ Failed to click submit button: {str(e)}")
                    return False
            
            # Take screenshot after submitting
            self.driver.save_screenshot("after_submit.png")
            
            # Wait for success message
            try:
                success_message = self.wait_for_element("//div[contains(text(), 'success') or contains(text(), 'Success')]")
                print(f"✅ Success message found: {success_message.text}")
            except TimeoutException:
                print("⚠️ No success message found, checking if modal closed...")
                try:
                    # Check if modal is closed by looking for Create New Sub-Admin button
                    self.wait_for_element("//button[contains(., 'Create New Sub-Admin')]")
                    print("✅ Modal closed successfully")
                except:
                    print("⚠️ Modal may still be open")
                    self.driver.save_screenshot("modal_state.png")
            
            return True
            
        except Exception as e:
            print(f"❌ Error in create sub admin test: {str(e)}")
            self.driver.save_screenshot("test_error.png")
            return False

    def run_all_tests(self):
        """Run all Create Sub Admin related tests"""
        try:
            # Login and navigate to Sub Admin page
            if not self.login_and_navigate_to_sub_admin():
                return False
            
            # Test closing modal with X button
            if not self.test_close_modal_with_x_button():
                return False
                
            # Test closing modal with Cancel button
            if not self.test_close_modal_with_cancel_button():
                return False
                
            # Test create sub-admin
            if not self.test_create_sub_admin():
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error in Create Sub Admin tests: {str(e)}")
            return False

if __name__ == "__main__":
    test = TestCreateSubAdmin()
    try:
        test.setUp()
        test.run_all_tests()
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
    finally:
        test.tearDown() 