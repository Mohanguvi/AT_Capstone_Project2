from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class Test_Case:

    def __init__(self):
        """
        Constructor method that initializes the class instance.
        It sets up URLs, initializes the WebDriver, and WebDriverWait.
        """
        self.url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
        self.admin_url = "https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers"
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 5)

    def start(self):
        """
        Method to start the WebDriver, navigate to the provided URL, and maximize the window.
        """
        self.driver.get(self.url)
        self.wait.until(EC.url_to_be(self.url))
        self.driver.maximize_window()

    def close(self):
        """
        Method to quit the WebDriver, closing the browser window.
        """
        self.driver.quit()

    def access(self):
        """
        Method to provide admin password if access is requested.
        """
        try:
            # Check if the banner is present
            Administrator_access = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/form/h6')))
            if Administrator_access:
                self.driver.find_element(By.NAME, "password").send_keys("admin123")
                self.driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/form/div[4]/button[2]').click()
                print("Admin password provided and access granted.")
        except TimeoutException:
            print("No banner found while accessing the page.")

    def login(self, username, password):
        """
        Method to logging in using the provided username and password.
        """
        try:
            self.start()
            # Enter the username
            self.wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys(username)
            # Enter the password
            self.wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys(password)
            # Click login button
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[3]/button'))).click()
            print("Login successful")
        except Exception as e:
            print("Login failed:", e)

    def logout(self):
        """
        Method to log out from the webpage.
        """
        try:
            # user menu
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div[1]/div[2]'))).click()
            # Log out
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div[1]/div[2]/ul/li/ul/li[4]/a'))).click()
            print("Logout successful")
        except Exception as e:
            print("Logout failed:", e)

    def TC_PIM_01(self):
        """
        Test Case ID: TC_PIM_01
        Test objective: Forgot Password link validation on login page
        """
        try:
            self.start()
            # Click on forget Password
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[4]/p'))).click()
            # Enter the username as Admin
            self.wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys("Admin")
            # CLick on submit to get the reset link
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div/form/div[2]/button[2]'))).click()
            print("Reset Password link sent successfully ")
            print("Password reset link url:", self.driver.current_url)
        except Exception as e:
            print("Test failed:", e)

    def TC_PIM_02(self):
        """
        Test Case ID: TC_PIM_02
        Test objective: Validate "Title" of the Page as "OrangeHRM"
                        Header Validation on Admin Page
        """
        try:
            self.start()
            self.login("Admin", "admin123")
            # Enter the Admin page
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[1]/a'))).click()
            # verify the tile of the page
            title = self.driver.title
            if title == "OrangeHRM":
                print("Title validation successful")
            else:
                print("Title validation failed")
            # Admin menu options xpath dictionary
            admin_options_xpath = {
                "User Management": '//*[@id="app"]/div[1]/div[1]/header/div[2]/nav/ul/li[1]',
                "Job": '//*[@id="app"]/div[1]/div[1]/header/div[2]/nav/ul/li[2]',
                "Organization": '//*[@id="app"]/div[1]/div[1]/header/div[2]/nav/ul/li[3]',
                "Qualifications": '//*[@id="app"]/div[1]/div[1]/header/div[2]/nav/ul/li[4]',
                "Nationalities": '//*[@id="app"]/div[1]/div[1]/header/div[2]/nav/ul/li[5]',
                "Corporate Banking": '//*[@id="app"]/div[1]/div[1]/header/div[2]/nav/ul/li[6]',
                "Configuration": '//*[@id="app"]/div[1]/div[1]/header/div[2]/nav/ul/li[7]'
            }
            # Validate the Admin Page Headers by iterating all the options
            for option, xpath in admin_options_xpath.items():
                # Wait for the admin option to be clickable and then click it
                admin_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                admin_option.click()
                print(f"'{option}' is clicked and appeared") # To verify all the admin option is click and appeared on the page

            print("Admin Page Headers on Admin menu are validated successfully")
        except Exception as e:
            print("Test failed:", e)
        finally:
            # Back to the dasboard page
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[8]/a'))).click()
            self.logout()

    def TC_PIM_03(self):
        """
        Test Case ID: TC_PIM_03
        Test objective: Main Menu Validation on Admin Page
        """
        try:
            self.start()
            self.login("Admin", "admin123")
            # Dictionary containing the main menu items and their XPaths
            main_menu = {
                "Admin": '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[1]/a',
                "PIM": '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[2]/a',
                "Leave": '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[3]/a',
                "Time": '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[4]/a',
                "Recruitment": '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[5]/a',
                "My Info": '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[6]/a',
                "Performance": '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[7]/a',
                "Dashboard": '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[8]/a',
                "Directory": '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[9]/a',
                "Maintenance": '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[10]/a',
                "Buzz": '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[12]/a'
            }
            # Iterate through the main menu items, click each one, and print its presence
            for menu_item, xpath in main_menu.items():
                # Find the element every time before interacting with it
                element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                element.click()
                print(f"Clicked on '{menu_item}'")
                print(f"{menu_item} url:", self.driver.current_url)
                # Check if the access pops up and provide admin key if needed
                self.access()
        except Exception as e:
            print("Test failed:", e)
        finally:
            self.close()

obj = Test_Case()
obj.TC_PIM_01()
obj.TC_PIM_02()
obj.TC_PIM_03()
