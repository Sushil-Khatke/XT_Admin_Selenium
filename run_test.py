from test_login import TestLogin

def main():
    test = TestLogin()
    try:
        # Run blank form submission test
        print("\nRunning Blank Form Submission Test...")
        blank_result = test.test_blank_form_submission()
        print("✅ Blank form test completed" if blank_result else "❌ Blank form test failed")
        
        # Run invalid credentials test
        print("\nRunning Invalid Credentials Test...")
        invalid_result = test.test_invalid_credentials()
        print("✅ Invalid credentials test completed" if invalid_result else "❌ Invalid credentials test failed")
        
        # Run input validation test
        print("\nRunning Input Validation Test...")
        validation_result = test.test_input_validation()
        print("✅ Input validation test completed" if validation_result else "❌ Input validation test failed")
        
        # Run successful login test
        print("\nRunning Successful Login Test...")
        login_result = test.test_login_validation()
        print("✅ Login test completed" if login_result else "❌ Login test failed")
        
    finally:
        test.close()

if __name__ == "__main__":
    main() 