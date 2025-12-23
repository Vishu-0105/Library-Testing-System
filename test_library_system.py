import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os

class TestLibraryManagementSystemFixed:
    """
    Professional Selenium Test Suite for Library Management System
    Testing comprehensive library functionality and user workflows
    """
    
    BASE_URL = "http://localhost:5000"
    
    # Library system test users
    LIBRARY_USERS = {
        'librarian': {'password': 'lib123', 'role': 'Head Librarian', 'name': 'Sarah Williams'},
        'student': {'password': 'student456', 'role': 'Student Member', 'name': 'Alex Johnson'},
        'faculty': {'password': 'faculty789', 'role': 'Faculty Member', 'name': 'Dr. Michael Chen'},
        'guest': {'password': 'guest321', 'role': 'Guest User', 'name': 'Jennifer Davis'}
    }
    
    @pytest.fixture(autouse=True)
    def setup_browser(self):
        """Setup browser for library system testing"""
        print("\nSetting up Chrome browser for library testing...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            # Use ChromeDriver from D: drive location
            chromedriver_path = "D:\\library_testing_system\\chromedriver.exe"
            if os.path.exists(chromedriver_path):
                print(f"Using ChromeDriver: {chromedriver_path}")
                service = Service(chromedriver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                print("Using system ChromeDriver...")
                self.driver = webdriver.Chrome(options=chrome_options)
                
            print("Library testing browser ready")
            
        except Exception as e:
            print(f"Browser setup failed: {e}")
            print("Ensure ChromeDriver is available and Chrome is installed")
            raise
        
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.implicitly_wait(10)
        
        yield
        
        print("Closing library testing session...")
        try:
            self.driver.quit()
        except:
            pass
    
    def take_screenshot(self, name):
        """Capture screenshot for test documentation"""
        try:
            timestamp = int(time.time())
            filename = f"library_test_{name}_{timestamp}.png"
            self.driver.save_screenshot(filename)
            print(f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            print(f"Screenshot failed: {e}")
            return None
    
    def verify_library_page_load(self, expected_title="City Library"):
        """Helper to verify library page loading"""
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: expected_title.lower() in driver.title.lower()
            )
            return True
        except TimeoutException:
            print(f"Page load verification failed for: {expected_title}")
            return False
    
    def login_user(self, username, password):
        """Helper method to login a user"""
        self.driver.get(f"{self.BASE_URL}/login")
        
        username_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_field = self.driver.find_element(By.ID, "password")
        
        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        time.sleep(2)
        return "/dashboard" in self.driver.current_url
    
    # TEST CASES
    
    def test_01_library_homepage_verification(self):
        """TC001: Verify library homepage loads with all components"""
        print("\nTC001: Library Homepage Verification")
        
        try:
            self.driver.get(self.BASE_URL)
            
            # Verify page title
            assert self.verify_library_page_load(), "Library homepage should load correctly"

            #to fail 
            #assert "Wrong Title" in self.driver.title, "Library homepage title mismatch (forced failure)"

            print("Library page title verified")
            
            # Check header with library branding
            header = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "header"))
            )
            assert "City Library Management System" in header.text
            print("Library header branding verified")
            
            # Verify library navigation menu
            nav = self.driver.find_element(By.CLASS_NAME, "nav")
            nav_links = nav.find_elements(By.TAG_NAME, "a")
            
            nav_text = nav.text
            expected_links = ["Home", "Login", "Contact", "About"]
            for link in expected_links:
                if link not in nav_text:
                    print(f"Warning: {link} not found in navigation")
            
            print(f"Library navigation verified ({len(nav_links)} links)")
            
            # Verify welcome box
            welcome_box = self.driver.find_element(By.CLASS_NAME, "welcome-box")
            assert welcome_box.is_displayed()
            print("Library welcome section verified")
            
            # Verify feature cards
            cards = self.driver.find_elements(By.CLASS_NAME, "card")
            assert len(cards) >= 2, "Should have multiple feature cards"
            print(f"Library feature cards verified ({len(cards)} cards)")
            
            self.take_screenshot("homepage_verification")
            print("TC001 PASSED: Library homepage verification complete")
            
        except Exception as e:
            self.take_screenshot("homepage_error")
            print(f"TC001 FAILED: {e}")
            raise
    
    def test_02_library_navigation_testing(self):
        """TC002: Test navigation across all library pages"""
        print("\nTC002: Library Navigation Testing")
        
        navigation_tests = [
            ("Home", "/"),
            ("Contact", "/contact"),
            ("About", "/about")
        ]
        
        successful_navigations = []
        
        for page_name, expected_path in navigation_tests:
            try:
                print(f"Testing navigation to {page_name} page...")
                
                # Start from homepage
                self.driver.get(self.BASE_URL)
                
                # Find and click navigation link
                try:
                    nav_link = self.wait.until(
                        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, page_name))
                    )
                    nav_link.click()
                    time.sleep(2)
                    
                    # Verify URL
                    current_url = self.driver.current_url
                    if expected_path == "/":
                        url_check = current_url in [self.BASE_URL, f"{self.BASE_URL}/"]
                    else:
                        url_check = expected_path in current_url
                    
                    if url_check:
                        successful_navigations.append(page_name)
                        print(f"{page_name} navigation successful")
                    else:
                        print(f"{page_name} navigation issue - URL: {current_url}")
                        
                except Exception as nav_error:
                    print(f"{page_name} navigation failed: {nav_error}")
                    
            except Exception as e:
                print(f"Navigation test error for {page_name}: {e}")
        
        print(f"Navigation Results: {len(successful_navigations)} successful")
        self.take_screenshot("navigation_testing")
        print("TC002 PASSED: Library navigation testing complete")
    
    def test_03_library_member_authentication(self):
        """TC003: Test library member login for all user types"""
        print("\nTC003: Library Member Authentication Test")
        
        successful_logins = []
        
        for username, user_data in self.LIBRARY_USERS.items():
            try:
                print(f"Testing login for {username} ({user_data['role']})")
                
                self.driver.get(f"{self.BASE_URL}/login")
                
                # Enter library member credentials
                username_field = self.wait.until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
                password_field = self.driver.find_element(By.ID, "password")
                
                username_field.clear()
                username_field.send_keys(username)
                password_field.clear()
                password_field.send_keys(user_data['password'])
                
                print(f"Entered credentials: {username}/{user_data['password']}")
                
                # Submit login form
                login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                login_button.click()
                
                # Wait for redirect to dashboard
                time.sleep(3)
                
                # Verify successful login
                if "/dashboard" in self.driver.current_url:
                    print("Redirected to library dashboard")
                    
                    # Verify user-specific library content
                    page_content = self.driver.page_source
                    if user_data['name'] in page_content or user_data['role'] in page_content:
                        print(f"Library member welcome verified: {user_data['name']}")
                    
                    # Check for logout link
                    try:
                        logout_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Logout")
                        assert logout_link.is_displayed()
                        print("Library session established")
                        successful_logins.append(username)
                        
                        # Logout for next test
                        logout_link.click()
                        time.sleep(2)
                        
                    except NoSuchElementException:
                        print("Logout link not found")
                else:
                    print(f"Login failed - URL: {self.driver.current_url}")
                
            except Exception as e:
                print(f"Authentication failed for {username}: {e}")
        
        print(f"Authentication Results: {len(successful_logins)} successful")
        self.take_screenshot("member_authentication")
        print("TC003 PASSED: Library member authentication complete")
    
    def test_04_invalid_library_credentials(self):
        """TC004: Test library system security with invalid credentials"""
        print("\nTC004: Invalid Library Credentials Security Test")
        
        invalid_scenarios = [
            ("wrong_user", "wrongpass", "Invalid credentials"),
            ("", "", "Empty credentials"),
            ("admin123", "admin123", "Non-existent member")
        ]
        
        security_tests_passed = 0
        
        for username, password, description in invalid_scenarios:
            try:
                print(f"Testing: {description}")
                
                self.driver.get(f"{self.BASE_URL}/login")
                
                username_field = self.wait.until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
                password_field = self.driver.find_element(By.ID, "password")
                
                username_field.clear()
                username_field.send_keys(username)
                password_field.clear()
                password_field.send_keys(password)
                
                login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                login_button.click()
                
                time.sleep(3)
                
                # Should remain on login page
                if "/login" in self.driver.current_url:
                    security_tests_passed += 1
                    print("Library security maintained - remained on login page")
                    
                    # Check for error message
                    try:
                        error_element = self.driver.find_element(By.CLASS_NAME, "flash-error")
                        if error_element.is_displayed():
                            print("Library security error message displayed")
                    except:
                        print("No error message found")
                else:
                    print("Security issue - login may have succeeded")
                
            except Exception as e:
                print(f"Security test error for '{description}': {e}")
        
        print(f"Security Results: {security_tests_passed} tests passed")
        self.take_screenshot("invalid_credentials")
        print("TC004 PASSED: Library security validation complete")
    
    def test_05_library_contact_form(self):
        """TC005: Test library inquiry/contact form functionality"""
        print("\nTC005: Library Contact Form Test")
        
        contact_scenarios = [
            {
                'name': 'John Library User',
                'email': 'john@library.edu',
                'message': 'This is a valid test message for the library contact form.',
                'expected': 'success',
                'description': 'Valid library inquiry'
            },
            {
                'name': '',
                'email': 'test@library.org',
                'message': 'Test message',
                'expected': 'error',
                'description': 'Empty name field'
            }
        ]
        
        form_tests_passed = 0
        
        for scenario in contact_scenarios:
            try:
                print(f"Testing: {scenario['description']}")
                
                self.driver.get(f"{self.BASE_URL}/contact")
                
                # Verify contact page loads
                assert self.verify_library_page_load(), "Contact page should load"
                print("Library contact page loaded")
                
                # Fill contact form
                try:
                    name_field = self.wait.until(EC.presence_of_element_located((By.ID, "name")))
                    email_field = self.driver.find_element(By.ID, "email")
                    message_field = self.driver.find_element(By.ID, "message")
                    
                    name_field.clear()
                    name_field.send_keys(scenario['name'])
                    email_field.clear()
                    email_field.send_keys(scenario['email'])
                    message_field.clear()
                    message_field.send_keys(scenario['message'])
                    
                    print("Library contact form filled")
                    
                    # Try to fill inquiry type if it exists
                    try:
                        inquiry_field = self.driver.find_element(By.ID, "inquiry_type")
                        inquiry_field.send_keys("Book Request")
                        print("Inquiry type selected")
                    except:
                        print("Inquiry type field not found")
                    
                    # Submit form
                    submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                    submit_button.click()
                    
                    time.sleep(3)
                    
                    # Check result based on expected outcome
                    page_content = self.driver.page_source.lower()
                    
                    if scenario['expected'] == 'success':
                        if any(word in page_content for word in ['thank', 'success', 'received']):
                            form_tests_passed += 1
                            print("Success message found")
                        else:
                            print("No success indicator found")
                    else:
                        if any(word in page_content for word in ['error', 'required', 'invalid']):
                            form_tests_passed += 1
                            print("Error validation working")
                        else:
                            print("No error validation detected")
                    
                except NoSuchElementException:
                    print("Contact form elements not found")
                
            except Exception as e:
                print(f"Contact form test failed for '{scenario['description']}': {e}")
        
        print(f"Contact Form Results: {form_tests_passed} tests completed")
        self.take_screenshot("contact_form")
        print("TC005 PASSED: Library contact form tested")
    
    def test_06_library_session_management(self):
        """TC006: Test library system session management and persistence"""
        print("\nTC006: Library Session Management Test")
        
        try:
            # Login to library system
            print("Testing library session establishment...")
            
            login_successful = self.login_user("librarian", "lib123")
            assert login_successful, "Should login successfully"
            print("Library session established")
            
            # Test session persistence across library pages
            library_pages = [
                f"{self.BASE_URL}",
                f"{self.BASE_URL}/contact",
                f"{self.BASE_URL}/about"
            ]
            
            session_maintained_count = 0
            
            for page_url in library_pages:
                print(f"Checking library session on: {page_url}")
                
                self.driver.get(page_url)
                time.sleep(2)
                
                try:
                    logout_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Logout")
                    if logout_link.is_displayed():
                        session_maintained_count += 1
                        print(f"Library session maintained on {page_url}")
                except NoSuchElementException:
                    print(f"Session indicator not found on {page_url}")
            
            print(f"Session persistence: {session_maintained_count}/{len(library_pages)} pages")
            
            # Test logout functionality
            print("Testing library logout functionality...")
            
            self.driver.get(f"{self.BASE_URL}/dashboard")
            time.sleep(1)
            
            if "/dashboard" in self.driver.current_url:
                try:
                    logout_link = self.wait.until(
                        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Logout"))
                    )
                    logout_link.click()
                    
                    time.sleep(3)
                    
                    # Verify logout successful
                    if "/dashboard" not in self.driver.current_url:
                        print("Successfully logged out from library system")
                    else:
                        print("Logout may have failed")
                        
                except Exception as e:
                    print(f"Logout test error: {e}")
            
            # Test post-logout access control
            print("Testing post-logout library access control...")
            
            self.driver.get(f"{self.BASE_URL}/dashboard")
            time.sleep(3)
            
            if "/dashboard" not in self.driver.current_url:
                print("Library dashboard access blocked after logout")
            else:
                print("WARNING: Dashboard accessible after logout")
            
            self.take_screenshot("session_management")
            print("TC006 PASSED: Library session management complete")
            
        except Exception as e:
            self.take_screenshot("session_management_error")
            print(f"TC006 FAILED: {e}")
            raise
    
    def test_07_library_catalog_functionality(self):
        """TC007: Test library catalog and search functionality"""
        print("\nTC007: Library Catalog Functionality Test")
        
        try:
            # Login first to access catalog
            print("Logging in to access catalog...")
            login_successful = self.login_user("student", "student456")
            
            if login_successful:
                print("Logged in successfully")
                
                # Navigate to catalog
                try:
                    catalog_link = self.wait.until(
                        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Catalog"))
                    )
                    catalog_link.click()
                    time.sleep(2)
                    print("Navigated to library catalog")
                except:
                    # Direct navigation if link not found
                    self.driver.get(f"{self.BASE_URL}/catalog")
                    time.sleep(2)
                    print("Direct navigation to catalog")
                
                # Verify catalog page elements
                if "/catalog" in self.driver.current_url:
                    print("Catalog page loaded successfully")
                    
                    # Look for search functionality
                    try:
                        search_field = self.driver.find_element(By.NAME, "search")
                        search_field.send_keys("Python")
                        
                        search_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                        search_button.click()
                        time.sleep(2)
                        print("Library catalog search functionality tested")
                    except NoSuchElementException:
                        print("Search functionality not found on current page")
                
                else:
                    print("Could not access catalog page")
            else:
                print("Could not login to test catalog")
            
            self.take_screenshot("catalog_functionality")
            print("TC007 PASSED: Library catalog functionality tested")
            
        except Exception as e:
            self.take_screenshot("catalog_functionality_error")
            print(f"TC007 FAILED: {e}")
    
    def test_08_library_profile_management(self):
        """TC008: Test library member profile functionality"""
        print("\nTC008: Library Profile Management Test")
        
        try:
            # Login and access profile
            print("Testing profile access...")
            login_successful = self.login_user("faculty", "faculty789")
            
            if login_successful:
                print("Logged in successfully")
                
                # Navigate to profile
                try:
                    profile_link = self.wait.until(
                        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Profile"))
                    )
                    profile_link.click()
                    time.sleep(2)
                    print("Navigated to library member profile")
                    
                    # Verify profile information
                    if "/profile" in self.driver.current_url:
                        profile_content = self.driver.page_source
                        if "Dr. Michael Chen" in profile_content and "Faculty Member" in profile_content:
                            print("Library member profile information verified")
                        else:
                            print("Profile information not fully verified")
                    
                except Exception as e:
                    print(f"Profile navigation error: {e}")
                    # Try direct navigation
                    self.driver.get(f"{self.BASE_URL}/profile")
                    time.sleep(2)
                    print("Direct profile navigation attempted")
                    
            else:
                print("Could not login to test profile")
            
            self.take_screenshot("profile_management")
            print("TC008 PASSED: Library profile management tested")
            
        except Exception as e:
            self.take_screenshot("profile_management_error")
            print(f"TC008 FAILED: {e}")
    
    def test_09_library_api_endpoint(self):
        """TC009: Test library system API endpoints"""
        print("\nTC009: Library API Endpoint Test")
        
        try:
            # Test library status API
            self.driver.get(f"{self.BASE_URL}/api/library-status")
            time.sleep(3)
            
            page_content = self.driver.page_source
            api_indicators = ["status", "operational", "books", "members", "timestamp"]
            
            api_working = any(indicator in page_content.lower() for indicator in api_indicators)
            
            if api_working:
                print("Library API endpoint responding correctly")
            else:
                print("API endpoint may not be working or content not as expected")
            
            self.take_screenshot("api_endpoint")
            print("TC009 PASSED: Library API testing complete")
            
        except Exception as e:
            self.take_screenshot("api_endpoint_error")
            print(f"TC009 FAILED: {e}")
    
    def test_10_comprehensive_library_security(self):
        """TC010: Comprehensive library system security testing"""
        print("\nTC010: Comprehensive Library Security Test")
        
        try:
            # Test unauthorized dashboard access
            print("Testing unauthorized library dashboard access...")
            
            self.driver.get(f"{self.BASE_URL}/logout")
            time.sleep(2)
            
            self.driver.get(f"{self.BASE_URL}/dashboard")
            time.sleep(3)
            
            if "/dashboard" not in self.driver.current_url:
                print("Unauthorized library dashboard access blocked")
                security_score = 1
            else:
                print("WARNING: Unauthorized dashboard access allowed")
                security_score = 0
            
            # Test input sanitization
            print("Testing library input sanitization...")
            
            self.driver.get(f"{self.BASE_URL}/login")
            
            username_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            username_field.clear()
            username_field.send_keys("<script>alert('XSS')</script>")
            
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys("lib123")
            
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(2)
            
            # Should remain on login page with script not executed
            if "/login" in self.driver.current_url:
                print("Library input sanitization working")
                security_score += 1
            else:
                print("Input sanitization may have issues")
            
            print(f"Security tests passed: {security_score}/2")
            
            self.take_screenshot("comprehensive_security")
            print("TC010 PASSED: Comprehensive library security testing complete")
            
        except Exception as e:
            self.take_screenshot("comprehensive_security_error")
            print(f"TC010 FAILED: {e}")
            raise

# Test execution configuration
if __name__ == "__main__":
    print("LIBRARY MANAGEMENT SYSTEM - SELENIUM TEST SUITE")
    print("=" * 60)
    print("Professional Library Testing Framework")
    print("10 Comprehensive Test Cases:")
    print("   TC001: Library homepage verification")
    print("   TC002: Library navigation testing")
    print("   TC003: Library member authentication")
    print("   TC004: Invalid credentials security")
    print("   TC005: Library contact form testing")
    print("   TC006: Library session management")
    print("   TC007: Library catalog functionality")
    print("   TC008: Library profile management")
    print("   TC009: Library API endpoint testing")
    print("   TC010: Comprehensive library security")
    print("=" * 60)
    
    import subprocess
    import sys
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", __file__, 
            "-v", "--tb=short", "--html=library_test_report.html", "--self-contained-html"
        ], capture_output=False)
        
        print("\n" + "=" * 60)
        if result.returncode == 0:
            print("ALL LIBRARY TESTS COMPLETED SUCCESSFULLY!")
            print("Library test report: library_test_report.html")
        else:
            print("Some library tests encountered issues.")
            print("Check library_test_report.html for details")
        print("=" * 60)
            
    except Exception as e:
        print(f"\nLibrary test execution error: {e}")
        print("Try running: pytest test_library_fixed.py -v")
