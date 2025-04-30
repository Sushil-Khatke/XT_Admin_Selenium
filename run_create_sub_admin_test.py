from test_create_sub_admin import TestCreateSubAdmin

def main():
    test = TestCreateSubAdmin()
    try:
        print("\nStarting Create Sub Admin Tests...")
        result = test.run_all_tests()
        if result:
            print("\n✅ All Create Sub Admin tests completed successfully!")
        else:
            print("\n❌ Some Create Sub Admin tests failed!")
    except Exception as e:
        print(f"\n❌ Error running Create Sub Admin tests: {str(e)}")
    finally:
        if hasattr(test, 'driver'):
            test.close()

if __name__ == "__main__":
    main() 