from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class Test_Case:

    def __init__(self):
        self.url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
        self.admin_url = "https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers"
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)

    def start(self):
        self.driver.get(self.url)
        self.wait.until(EC.url_to_be(self.url))
        self.driver.maximize_window()

    def close(self):
        self.driver.quit()

    def login(self, username, password):
        """
        Logging in using the provided username and password.
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
        Log out from the webpage.
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
        Test objective: Header Validation on Admin Page
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

            admin_options_xpath = {
                "User Management": '//*[@id="app"]/div[1]/div[1]/header/div[2]/nav/ul/li[1]',
                "Job": '//*[@id="app"]/div[1]/div[1]/header/div[2]/nav/ul/li[2]',
                "Organization": '//*[@id="menu_admin_Organization"]',
                "Qualifications": '//*[@id="menu_admin_Qualifications"]',
                "Nationalities": '//*[@id="menu_admin_nationality"]',
                "Corporate Banking": '//*[@id="menu_admin_BankInfo"]',
                "Configuration": '//*[@id="menu_admin_Configuration"]'
            }

            for option, xpath in admin_options_xpath.items():
                self.driver.find_element(By.XPATH, xpath).click()
                print(f"Clicked on '{option}'")

                print("All admin options clicked successfully")
        except Exception as e:
            print("Test failed:", e)
        finally:
            self.close()

    def test_TC_PIM_03(self, username, password):
        """
        Test Case ID: TC_PIM_03
        Test objective: Main Menu Validation on Admin Page
        """
        try:
            self.start("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
            self.wait.until(EC.visibility_of_element_located((By.ID, "txtUsername"))).send_keys(username)
            self.wait.until(EC.visibility_of_element_located((By.ID, "txtPassword"))).send_keys(password)
            self.driver.find_element_by_id("btnLogin").click()
            self.wait.until(EC.visibility_of_element_located((By.ID, "menu_admin_viewAdminModule"))).click()
            admin_menu = ["Admin", "PIM", "Leave", "Time", "Recruitment", "My Info", "Performance",
                          "Dashboard", "Directory", "Maintenance", "Buzz"]
            for menu_item in admin_menu:
                element = self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, menu_item)))
                if element.is_displayed():
                    print(f"Menu item '{menu_item}' is displayed")
                else:
                    print(f"Menu item '{menu_item}' is not displayed")
        except Exception as e:
            print("Test failed:", e)
        finally:
            self.close()

# Usage
obj = Test_Case()
obj.TC_PIM_01()
obj.TC_PIM_02()
obj.close()

