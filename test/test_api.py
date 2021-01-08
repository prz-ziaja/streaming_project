import unittest

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://localhost")

    def testCorrectLoginIncorrectPassword(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("wrongpass")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Login']").click()
        msg_field = self.driver.find_elements_by_xpath("//div[@class='msg']")
        msg_field_text = msg_field.pop().text
        assert msg_field_text == 'Incorrect username/password!'

    def testCorrectLoginEmptyPassword(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Login']").click()
        assert password_field.get_attribute("validationMessage") == "Please fill out this field."

    def testEmptyLoginCorrectPassword(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("test")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Login']").click()
        assert username_field.get_attribute("validationMessage") == "Please fill out this field."

    def testSucceedingLogin(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("test")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Login']").click()
        assert WebDriverWait(self.driver, 5).until(EC.title_is("Home"))

    def tearDown(self):
        self.driver.close()


class TestRegister(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1/pythonlogin/register")

    def testEmptyUsernameCorrectPasswordCorrectEmail(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("test")

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()
        email_field.send_keys("test@test.com")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        assert username_field.get_attribute("validationMessage") == "Please fill out this field."

    def testCorrectUsernameEmptyPasswordCorrectEmail(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()
        email_field.send_keys("test@test.com")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        assert password_field.get_attribute("validationMessage") == "Please fill out this field."

    def testCorrectUsernameCorrectPasswordEmptyEmail(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("pass")

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        assert email_field.get_attribute("validationMessage") == "Please fill out this field."

    def testCorrectUsernameCorrectPasswordIncorrectEmail(self):
        """
        "test@test", "@test.com", "test@@test.com", "test.com@"
        """
        emails_to_test = ["test@test", "@test.com", "test@@test.com", "test.com@"]
        for email in emails_to_test:
            assert self.checkMail(email)

    def checkMail(self, email):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("testuser")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("testuser")

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()
        email_field.send_keys(email)

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        msg_field = self.driver.find_elements_by_xpath("//div[@class='msg']")
        msg_field_text = msg_field.pop().text
        return msg_field_text == 'Invalid email address!'

    def testUsedCredentials(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("test")

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()
        email_field.send_keys("test@test.com")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        msg_field = self.driver.find_elements_by_xpath("//div[@class='msg']")
        msg_field_text = msg_field.pop().text
        return msg_field_text == 'Account already exists!'

    def testIncorrectUsernameCorrectPasswordCorrectEmail(self):
        """
        "ad@m2020", "test2020!"
        """
        usernames_to_test = ["ad@m2020", "test2020!", "test%", "test20&"]
        for username in usernames_to_test:
            assert self.checkUsername(username)

    def checkUsername(self, username):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys(username)

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("pass")

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()
        email_field.send_keys("test@example.com")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        msg_field = self.driver.find_elements_by_xpath("//div[@class='msg']")
        msg_field_text = msg_field.pop().text
        return msg_field_text == 'Username must contain only characters and numbers!'

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
