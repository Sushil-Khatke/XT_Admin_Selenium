from test_sub_admin import TestSubAdmin

def main():
    test = TestSubAdmin()
    try:
        print("\nStarting Sub Admin Tests...")
        result = test.run_all_tests()
        if result:
            print("\n✅ All Sub Admin tests completed successfully!")
        else:
            print("\n❌ Some Sub Admin tests failed!")
    except Exception as e:
        print(f"\n❌ Error running Sub Admin tests: {str(e)}")
    finally:
        if hasattr(test, 'driver'):
            test.close()

if __name__ == "__main__":
    main() 